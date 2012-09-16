from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural = 'categories'

	def __unicode__(self):
		return self.name


class Committee(models.Model):
	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=20, unique=True)
	description = models.TextField()
	category = models.ForeignKey(Category)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('committee_view', [self.slug])

	class Meta:
		ordering = ('category', 'id')


class CommitteeApplication(models.Model):
	"""
	An abstract base class used by all committee applications
	"""
	class Meta:
		abstract = True

	name = models.CharField(max_length=100)
	school = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	head_delegate_name = models.CharField(max_length=100, verbose_name="Name of head delegate")
	field_of_study = models.CharField(max_length=100)
	previous_mun_experience = models.TextField(verbose_name="Describe your previous Model UN experience.")

	def __unicode__(self):
		return "%s for %s" % (self.name, self.committee_name)


class AdHocApplication(CommitteeApplication):
	# This is used solely for display. Can't actually use self.committee.
	committee_name = 'the Ad-Hoc Committee of the Secretary-General'

	what_topic = models.TextField(verbose_name="If you were given the opportunity to select the Ad-Hoc committee topic, what topic would you choose?")
	world_leader_coffee = models.TextField(verbose_name="Who is one living world leader you would like to have a coffee talk with and why?")
	no_background_knowledge = models.TextField(verbose_name="What will you do if you have no background knowledge of the chosen topic?")
	# There must be a better way to do this?
	why_choose_you = models.TextField(verbose_name="Why should you be chosen as a member of %s? What skills can you bring to this committee?" % committee_name)


class BRICSApplication(CommitteeApplication):
	committee_name = 'the BRICS Summit'

	teammate_1_name_email = models.CharField(max_length=255, verbose_name="Name and email of teammate 1")
	teammate_2_name_email = models.CharField(max_length=255, verbose_name="Name and email of teammate 2")
	what_topic = models.TextField(verbose_name="What would you choose as the BRICS Summit topic of discussion and why?")
	why_choose_you = models.TextField(verbose_name="Why should you be chosen as a member of %s? What skills can you bring to this committee?" % committee_name)
	world_leader_coffee = models.TextField(verbose_name="Who is one living world leader you would like to have a coffee talk with and why?")
	significance_of_brics = models.TextField(verbose_name="Describe the significance of the BRICS nations in less than 250 words.")


class NixonApplication(CommitteeApplication):
	committee_name = "the Nixon Interviews Joint Crisis"

	why_choose_you = models.TextField(verbose_name="Why should you be chosen as a member of %s? What skills can you bring to this committee?" % committee_name)
	significance = models.TextField(verbose_name="What is the significance of the interviews held between David Frost and Richard Nixon?")
	which_side = models.TextField(verbose_name="Which side of the joint crisis would you prefer to be on and why?")
	frost_ask_nixon = models.TextField(verbose_name="If you were David Frost, what would you have asked Richard Nixon?")
	nixon_presidency = models.TextField(verbose_name="Describe Richard Nixon's presidency in less than 250 words.")


class WallStreetApplication(CommitteeApplication):
	committee_name = "Wall Street 2008"

	facebook_ipo = models.TextField(verbose_name="In May 2012, Facebook, Inc. held its initial public offering (IPO) at an unprecedented valuation for an internet corporation. Since then, it is arguable that Facebook's IPO failed to match traders' expectations. Do you agree? Also, what are the long-term and the short-term forecasts for Facebook's stock in your opinion? Explain in less than two hundred words.")
	british_libor = models.TextField(verbose_name="This summer, the British financial system faced heavy scrutiny and damaging accusations of manipulation of the London Interbank Offered Rate (LIBOR). Should the British government get involved? What are the implications of this scandal? Explain in less than two hundred words.")
	bull_bear = models.TextField(verbose_name="Are you bull-ish or bear-ish? Explain in two sentences or less.")
