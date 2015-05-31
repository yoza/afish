"""
Accomulate qrecipe app urls
"""

from django.conf.urls import patterns, url

from home.views import IndexView


urlpatterns = patterns(
    '',
    url(r'^(?P<slug>home)?(/)?$',
        IndexView.as_view(), name='home'),
    )
