from django.db import models
import markdown
import os

class Page(models.Model):
	# Used in the URL and on the filesystem (no spaces)
	short_name = models.CharField(max_length=20, unique=True)
	# Used for the menu (lowercase), and as the page title
	long_name = models.CharField(max_length=50)
	# Will show the <h1> with the title AND the mini breadcrumbs navbar shit
	show_nav = models.BooleanField(default=True)
	# Will populate the {{ content }} variable in the template (custom or default)
	content = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.long_name

class ParentPage(Page):
	class Meta:
		ordering = ['position']

	# Determines the ordering in the menu bar
	position = models.PositiveIntegerField(unique=True)

class SubPage(Page):
	class Meta:
		ordering = ['position']
		unique_together = ('position', 'parent')

	parent = models.ForeignKey(ParentPage, related_name="subpages")
	# Has to be defined here because, different "self"s etc
	position = models.PositiveIntegerField()
