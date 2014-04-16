from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nba_reddit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^threads/', 'live_stream.views.retrieve_threads', name="retrieve_threads"),
    url(r'^comments/', 'live_stream.views.retrieve_comments', name="retrieve_comments"),
    url(r'^redirect_url', 'live_stream.views.redirect_url', name="redirect_url"),
    url(r'^retrieve', 'live_stream.views.retrieve', name="retrieve"),
)
