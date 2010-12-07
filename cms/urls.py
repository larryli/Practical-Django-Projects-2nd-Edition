from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from coltrane.models import Entry

entry_info_dict = {
	'queryset': Entry.objects.all(),
	'date_field': 'pub_date',
}

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	(r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': '/home/gavin/Documents/Practical-Django-Projects-2nd-Edition/scripts/tiny_mce/'}),

	(r'^weblog/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
		'django.views.generic.date_based.object_detail', entry_info_dict),
	(r'^weblog/$', 'coltrane.views.entries_index'),

	(r'^search/$', 'cms.search.views.search'),
	(r'', include('django.contrib.flatpages.urls')),
)
