"""
rest framevork urls

"""

from django.conf.urls import patterns, url, include

from events.views import rest_views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'events/geosearch', rest_views.GeoViewSet)
router.register(r'events', rest_views.EventViewSet)


urlpatterns = patterns(
    '', url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))
    )
