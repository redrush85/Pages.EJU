from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'urlcatalog.Catalog.views.index'),
    url(r'^list/', 'urlcatalog.Catalog.views.detailedlist'),
    url(r'^url/(\d+)/$', 'urlcatalog.Catalog.views.showurl'),
    url(r'^category/(\d+)/$', 'urlcatalog.Catalog.views.showcategory'),
    url(r'^search', 'urlcatalog.Catalog.views.search'),
    # url(r'^urlcatalog/', include('urlcatalog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    #url(r'^accounts/', include('registration.backends.default.urls')),
)
