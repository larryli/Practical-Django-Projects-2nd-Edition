import datetime

from django.db import models
from django.contrib.auth.models

from markdown import markdown
from tagging.fields import TagField

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

	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	HIDDEN_STATUS = 3
	STATUS CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
		(HIDDEN_STATUS, 'Hidden'),
	)

	# core fields
	title = models.CharField(max_length=250)
	excerpt = models.TextField(blank=True)
	body = models.TextField()
	pub_date = models.DateTimeField(default=datetime.datetime.now)
	
	# fields to store generated html
	excerpt_html = models.TextField(editable=False, blank=True)
	body_html = models.TextField(editable=False, blank=True)
	
	# metadata
	author = models.ForeignKey(User)
	enable_comments = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	slug = models.SlugField(unique_for_date='pub_date')
	status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)

	# categorization
	categories = models.ManyToManyField(Category)
	tags = TagField()

	class Meta:
		ordering = ['-pub_date']
		verbose_name_plural = 'Entries'

	def __unicode__(self):
		return self.title

	def save(self, force_insert=False, force_update=False):

		self.body_html = markdown(self.body)

		if self.excerpt:
			self.excerpt_html = markdown(self.excerpt)

		super(Entry, self).save(force_insert, force_update)
	
	def get_absolute_url(self):
		return '/weblog/%s/%s/' % (self.pub_date.strftime('%Y/%b/%d').lower(), self.slug)
