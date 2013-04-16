from django.db import models

SIGNUP_CATEGORIES = (
	(1, 'Staff'),
	(2, 'Charge')
)

class Person(models.Model):
	class Meta:
		ordering = ['category']

	email = models.EmailField(max_length=254, unique=True)
	name = models.CharField(max_length=50)
	category = models.IntegerField(choices=SIGNUP_CATEGORIES)

	def __unicode__(self):
		return '%s <%s>' % (self.name, self.email)
