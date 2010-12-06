import datetime

from django.db import models
from django.contrib.auth.models


class Category(models.Model):

	title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
	slug = models.SlugField(unique=True, help_text='Suggested value automatically generated from title. Must be unique.')
	description = models.TextField()

	class Meta:
		ordering = ['title']
		verbose_name_plural = "Categories"


	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return '/categories/%s/' % self.slug


class Entry(models.Model):

	title = models.CharField(max_length=250)
	slug = models.SlugField(unique_for_date='pub_date')
	excerpt = models.TextField(blank=True)
	body = models.TextField()
	author = models.ForeignKey(User)
	pub_date = models.DateTimeField(default=datetime.datetime.now)


