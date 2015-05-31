from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^api/', include('events.urls.rest_urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('home.urls')),
)
