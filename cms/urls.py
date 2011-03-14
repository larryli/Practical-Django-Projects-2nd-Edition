import os
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	(r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'scripts/tiny_mce/')}),

	(r'^weblog/categories/', include('coltrane.urls.categories')),
	(r'^weblog/links/', include('coltrane.urls.links')),
	(r'^weblog/tags/', include('coltrane.urls.tags')),
	(r'^weblog/', include('coltrane.urls.entries')),

	(r'^search/$', 'cms.search.views.search'),
	(r'', include('django.contrib.flatpages.urls')),
)
