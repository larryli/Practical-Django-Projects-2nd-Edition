from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	(r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': '/home/gavin/Documents/Practical-Django-Projects-2nd-Edition/scripts/tiny_mce/'}),

	(r'^weblog/', include('coltrane.urls')),

	(r'^search/$', 'cms.search.views.search'),
	(r'', include('django.contrib.flatpages.urls')),
)
