from django.conf.urls import patterns, include, url

urlpatterns = patterns('app.views',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'index_view'),
)
