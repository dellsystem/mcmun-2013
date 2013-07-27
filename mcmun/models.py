from decimal import Decimal
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver

from mcmun.utils import generate_random_password
from mcmun.constants import MIN_NUM_DELEGATES, MAX_NUM_DELEGATES, COUNTRIES, DELEGATION_FEE, YESNO, HOWYOUHEAR
from mcmun.tasks import send_email, generate_invoice
from committees.models import Committee, ScholarshipIndividual


# test
class RegisteredSchool(models.Model):
	class Meta:
		ordering = ['school_name']

	school_name = models.CharField(max_length=100, unique=True)
	first_time = models.BooleanField(choices=YESNO)
	how_you_hear = models.CharField(max_length=14, choices=HOWYOUHEAR, null=True, blank=True)
	another_school = models.CharField(max_length=100, null=True, blank=True)
	other_method = models.CharField(max_length=100, null=True, blank=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=50, unique=True)
	delegate_email = models.EmailField(max_length=50, null=True, blank=True)
	other_email = models.EmailField(max_length=255, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	mail_address = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	province_state = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	advisor_phone = models.CharField(max_length=20)
	fax = models.CharField(max_length=20, null=True, blank=True)
	country = models.CharField(max_length=2, choices=COUNTRIES)


	num_delegates = models.IntegerField(default=1, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES + 1)])
	amount_paid = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)

	# Needs a boolean field anyway to make the admin interface better
	is_approved = models.BooleanField(default=False, verbose_name="Approve school")

	# Committee preferences. SO BAD
	committee_1 = models.ForeignKey(Committee, limit_choices_to= (Q(slug='automobile') | Q(slug='igf') | Q(slug='epha') | Q(slug='emirs') | Q(slug='undef') | Q(slug='tunisian') | Q(slug='newspaper') | Q(slug='nfl') |Q(slug='korean') | Q(slug='war') | Q(slug='ad-hoc') | Q(slug='punic') | Q(slug='robinh')), related_name="school_1")
	committee_2 = models.ForeignKey(Committee, limit_choices_to= (Q(slug='automobile') | Q(slug='igf') | Q(slug='epha') | Q(slug='emirs') | Q(slug='undef') | Q(slug='tunisian') | Q(slug='newspaper') | Q(slug='nfl') |Q(slug='korean') | Q(slug='war') | Q(slug='ad-hoc') | Q(slug='punic') | Q(slug='robinh')), related_name="school_2")
	committee_3 = models.ForeignKey(Committee, limit_choices_to= (Q(slug='automobile') | Q(slug='igf') | Q(slug='epha') | Q(slug='emirs') | Q(slug='undef') | Q(slug='tunisian') | Q(slug='newspaper') | Q(slug='nfl') |Q(slug='korean') | Q(slug='war') | Q(slug='ad-hoc') | Q(slug='punic') | Q(slug='robinh')), related_name="school_3")
	committee_4 = models.ForeignKey(Committee, limit_choices_to= (Q(slug='automobile') | Q(slug='igf') | Q(slug='epha') | Q(slug='emirs') | Q(slug='undef') | Q(slug='tunisian') | Q(slug='newspaper') | Q(slug='nfl') |Q(slug='korean') | Q(slug='war') | Q(slug='ad-hoc') | Q(slug='punic') | Q(slug='robinh')), related_name="school_4")


	# Country preferences.
	country_1 = models.CharField(max_length=2, choices=COUNTRIES)
	country_2 = models.CharField(max_length=2, choices=COUNTRIES)
	country_3 = models.CharField(max_length=2, choices=COUNTRIES)
	country_4 = models.CharField(max_length=2, choices=COUNTRIES)
	country_5 = models.CharField(max_length=2, choices=COUNTRIES)
	country_6 = models.CharField(max_length=2, choices=COUNTRIES)
	country_7 = models.CharField(max_length=2, choices=COUNTRIES)
	country_8 = models.CharField(max_length=2, choices=COUNTRIES)
	country_9 = models.CharField(max_length=2, choices=COUNTRIES)
	country_10 = models.CharField(max_length=2, choices=COUNTRIES)

	experience = models.TextField(null=True, blank=True)
	mcgill_tours = models.IntegerField(default=0, choices=[(n, n) for n in xrange(MIN_NUM_DELEGATES, MAX_NUM_DELEGATES + 1)])
	disclaimer = models.BooleanField(choices=YESNO, default=True)
	account = models.ForeignKey(User, null=True)

	use_online_payment = models.BooleanField(choices=YESNO)
	use_priority = models.BooleanField(default=True)
	def has_prefs(self):
		return (self.committee_1 or self.committee_2 or self.committee_3 or
			self.committee_4)


	def is_international(self):
		"""
		Checks if the institution is "international" (i.e. outside North America).
		"""
		return self.country != 'CA' and self.country != 'US'

	def get_payment_type(self):
		if self.use_priority:
			payment_type = 'priority'
		else:
			payment_type = 'regular'

		return payment_type

	def get_currency(self):
		"""
		Returns CAD if the institution is Canadian, USD otherwise.
		"""
		return 'CAD' if self.country == 'CA' else 'USD'

	def get_tour_fee(self):
		return (self.mcgill_tours * 2)

	def get_tour_fee_str(self):
		return "%.2f" % (self.mcgill_tours * 2)


	# These are messy. Deal with it another time.
	def get_total_convenience_fee(self):
		return "%.2f" % ((self.num_delegates * self.get_delegate_fee() + DELEGATION_FEE + self.get_tour_fee())  * 0.03)

	def get_deposit_convenience_fee(self):
		return "%.2f" % ((DELEGATION_FEE + (self.get_delegate_fee() * self.num_delegates) * 0.5) * 0.03)

	def get_remainder_convenience_fee(self):
		return "%.2f" % ((self.get_delegate_fee() * self.num_delegates * 0.5) * 0.03)

	def add_convenience_fee(self, number):
		"""
		Incorporates a 3% convenience fee into the number given iff the school
		has selected online payment and has registered after Sept 1.
		"""
		if self.use_online_payment:
			return number * 1.03
		else:
			return number

	def get_delegate_fee(self):
		delegate_fee = 85 if self.use_priority else 90

		return delegate_fee

	def get_total_delegate_fee(self):
		return self.get_delegate_fee() * self.num_delegates

	def get_total_owed(self):
		total_owed = self.num_delegates * self.get_delegate_fee() + DELEGATION_FEE + self.get_tour_fee() - float(self.amount_paid)

		return "%.2f" % self.add_convenience_fee(total_owed)

	def get_amount_paid(self):
		return "$%s" % self.amount_paid

	def get_deposit(self):
		deposit = DELEGATION_FEE + (self.get_delegate_fee() * self.num_delegates) * 0.5

		return "%.2f" % self.add_convenience_fee(deposit)

	def get_remainder(self):
		remainder = self.get_delegate_fee() * self.num_delegates * 0.5

		return "%.2f" % self.add_convenience_fee(remainder)

	def amount_owed(self):
		return "$%s" % self.get_total_owed()

	def send_success_email(self):
		# Send out email to user (receipt of registration)
		receipt_subject = 'Successful registration for SSUNS 2013'
		receipt_message_filename = 'registration_success'
		receipt_context = {
			'first_name': self.first_name,
			'school_name': self.school_name,
		}

		send_email.delay(receipt_subject, receipt_message_filename, [self.email], context=receipt_context)

		# Send out email to Serena, myself (link to approve registration)
		approve_subject = 'New registration for SSUNS'
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

	def has_unfilled_assignments(self):
		return any(not c.is_filled() for c in self.committeeassignment_set.all())

	def __unicode__(self):
		return self.school_name


class ScholarshipApp(models.Model):
	school = models.OneToOneField(RegisteredSchool)
	# club_name = models.CharField(max_length=100)
	# num_days_staying = models.IntegerField()
	new_school = models.BooleanField()
	international = models.BooleanField()
	# previously_attended = models.BooleanField()
	previous_scholarship_amount = models.IntegerField(null=True, blank=True)
	previous_scholarship_year = models.IntegerField(null=True, blank=True)
	impact_on_delegation = models.TextField()
	principles_of_organisation = models.TextField()
	importance_of_ssuns = models.TextField()
	# how_funding_works = models.TextField()
	# other_funding_sources = models.TextField()
	# budget = models.TextField()
	other_information = models.TextField(null=True, blank=True)
	# co_head_name = models.CharField(max_length=100, null=True, blank=True)
	# co_head_email = models.EmailField(max_length=255, null=True, blank=True)
	# co_head_phone = models.CharField(max_length=20, null=True, blank=True)

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
		username = instance.email[:30]
		new_account = User.objects.create_user(username=username, password=password)
		instance.account = new_account

		instance.send_invoice_email(new_account.username, password)
