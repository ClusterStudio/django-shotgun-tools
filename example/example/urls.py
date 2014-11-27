from django.conf.urls import patterns, include, url
from django.contrib import admin
from django_sgtk.api import sg_api

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(sg_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
