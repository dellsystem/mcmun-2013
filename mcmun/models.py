from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver

from mcmun.utils import generate_random_password
from mcmun.constants import MIN_NUM_DELEGATES, MAX_NUM_DELEGATES, COUNTRIES, DELEGATION_FEE
from mcmun.tasks import send_email, generate_invoice


class RegisteredSchool(models.Model):
	school_name = models.CharField(max_length=100, unique=True)
	address = models.CharField(max_length=255)
	country = models.CharField(max_length=2, choices=COUNTRIES)

	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=255, unique=True)
	phone_number = models.CharField(max_length=20)

	num_delegates = models.IntegerField(default=1, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES + 1)])
	use_online_payment = models.BooleanField()
	use_tiered = models.BooleanField()
	use_priority = models.BooleanField()

	amount_paid = models.IntegerField(default=0)

	# Only set iff the user has been approved
	account = models.ForeignKey(User, null=True)
	# Needs a boolean field anyway to make the admin interface better
	is_approved = models.BooleanField(default=False, verbose_name="Approve school")

	def is_international(self):
		"""
		Checks if the institution is "international" (i.e. outside North America).
		"""
		return self.country != 'CA' and self.country != 'US'

	def get_payment_type(self):
		if self.is_international():
			payment_type = 'international'
		elif self.use_priority:
			payment_type = 'priority'
		else:
			payment_type = 'regular'

		return payment_type

	def get_currency(self):
		"""
		Returns CAD if the institution is Canadian, USD otherwise.
		"""
		return 'CAD' if self.country == 'CA' else 'USD'

	def get_delegate_fee(self):
		if self.is_international():
			delegate_fee = 50
		else:
			delegate_fee = 80 if self.use_priority else 95

		return delegate_fee

	def get_total_delegate_fee(self):
		return self.get_delegate_fee() * self.num_delegates

	def get_total_owed(self):
		return "%.2f" % (self.num_delegates * self.get_delegate_fee() + DELEGATION_FEE)

	def get_deposit(self):
		return "%.2f" % (DELEGATION_FEE + (self.get_delegate_fee() * self.num_delegates) * 0.5)

	def get_remainder(self):
		return "%.2f" % (self.get_delegate_fee() * self.num_delegates * 0.5)

	def amount_owed(self):
		if self.use_tiered:
			return "$%s (%s deposit, %s remainder)" % (self.get_total_owed(), self.get_deposit(), self.get_remainder())
		else:
			return "$%s" % self.get_total_owed()

	def send_success_email(self):
		# Send out email to user (receipt of registration)
		receipt_subject = 'Successful registration for McMUN 2013'
		receipt_message_filename = 'registration_success'
		receipt_context = {
			'first_name': self.first_name,
			'school_name': self.school_name,
		}

		send_email.delay(receipt_subject, receipt_message_filename, [self.email], context=receipt_context)

		# Send out email to Stysis, myself (link to approve registration)
		approve_subject = 'New registration for McMUN'
		approve_message_filename = 'registration_approve'
		approve_context = {
			'first_name': self.first_name,
			'last_name': self.last_name,
			'school_name': self.school_name,
			'email': self.email,
			'admin_url': settings.ADMIN_URL,
			'school_id': self.id,
		}

		send_email.delay(approve_subject, approve_message_filename, [settings.IT_EMAIL, settings.CHARGE_EMAIL], context=approve_context)

	def send_invoice_email(self, username, password):
		print "about to delay the generate_invoice task"
		generate_invoice.delay(self.id, username, password)

	def __unicode__(self):
		return self.school_name


class ScholarshipApp(models.Model):
	school = models.OneToOneField(RegisteredSchool)
	club_name = models.CharField(max_length=100)
	num_days_staying = models.IntegerField()
	previously_attended = models.BooleanField()
	previous_scholarship_amount = models.IntegerField(null=True, blank=True)
	previous_scholarship_year = models.IntegerField(null=True, blank=True)
	impact_on_delegation = models.TextField()
	principles_of_organisation = models.TextField()
	importance_of_mcmun = models.TextField()
	how_funding_works = models.TextField()
	other_funding_sources = models.TextField()
	budget = models.TextField()
	other_information = models.TextField(null=True, blank=True)
	co_head_name = models.CharField(max_length=100, null=True, blank=True)
	co_head_email = models.EmailField(max_length=255, null=True, blank=True)
	co_head_phone = models.CharField(max_length=20, null=True, blank=True)

	def __unicode__(self):
		return self.school.school_name


@receiver(models.signals.pre_save, sender=RegisteredSchool, dispatch_uid="approve_schools")
def approve_schools(sender, instance, **kwargs):
	"""
	When a school is approved, create an account for it (with a random
	password) and send an email containing the login info as well as the
	invoice (attached as a PDF).
	"""
	if instance.is_approved and instance.account is None:
		# School does not have an account. Make one!
		password = generate_random_password()
		new_account = User.objects.create_user(username=instance.email,
											   password=password)
		instance.account = new_account

		instance.send_invoice_email(new_account.username, password)
