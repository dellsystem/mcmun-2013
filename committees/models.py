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
