import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

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

	@models.permalink
	def get_absolute_url(self):
		#return '/categories/%s/' % self.slug
		return ('coltrane_category_detail', (), { 'slug': self.slug })

	def live_entry_set(self):
		#from coltrane.models import Entry
		return self.entry_set.filter(status=Entry.LIVE_STATUS)


class LiveEntryManager(models.Manager):

	def get_query_set(self):
		return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)


class Entry(models.Model):

	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	HIDDEN_STATUS = 3
	STATUS_CHOICES = (
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
	
	@models.permalink
	def get_absolute_url(self):
		return ('coltrane_entry_detail', (),
			{'year': self.pub_date.strftime('%Y'),
			 'month': self.pub_date.strftime('%b').lower(),
			 'day': self.pub_date.strftime('%d'),
			 'slug': self.slug})

	live = LiveEntryManager()
	objects = models.Manager()


class Link(models.Model):

	url = models.URLField(unique=True)
	title = models.CharField(max_length=250)
	slug = models.SlugField(unique_for_date='pub_date', help_text='Must be unique for the publication date.')
	description = models.TextField(blank=True)
	description_html = models.TextField(editable=False, blank=True)
	via_name = models.CharField(
		'Via',
		max_length=250,
		blank=True,
		help_text='The name of the person whose site you spotted the link on. Optional.')
	via_url = models.URLField(
		'Via URL',
		blank=True,
		help_text='The URL of the site where you spotted the link. Optional.')
	tags = TagField()

	
	# metadata
	enable_comments = models.BooleanField(default=True)
	post_elsewhere = models.BooleanField(
		'Post to Delicious',
		default=True,
		help_text='If checked, this link will also be posted to your del.icio.us account.')
	posted_by = models.ForeignKey(User)
	pub_date = models.DateTimeField(default=datetime.datetime.now)


	class Meta:
		ordering = ['-pub_date']


	def __unicode__(self):
		return self.title

	def save(self):

		if self.description:
			self.description_html = markdown(self.description)

		if not self.id and self.post_elsewhere:
			pass

			# del.icio.us authentication doesn't work right now
			# I started playing with twitter
			# but it's a real pain in the ass for a simple tutorial

#			import pydelicious
#			from django.utils.encoding import smart_str

#			pydelicious.add(
#				settings.DELICIOUS_USER,
#				settings.DELICIOUS_PASSWORD,
#				smart_str(self.url),
#				smart_str(self.title),
#				smart_str(self.tags))

		super(Link, self).save()

	@models.permalink
	def get_absolute_url(self):

		return('coltrane_link_detail', (),
			{'year': self.pub_date.strftime('%Y'),
			 'month': self.pub_date.strftime('%b').lower(),
			 'day': self.pub_date.strftime('%d'),
			 'slug': self.slug})
