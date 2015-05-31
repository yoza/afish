import json as simplejson

from django.conf import settings
from django.shortcuts import get_object_or_404

from geopy.distance import great_circle

from events.api.serializers import EeventSerializer, InstanceSerializer
from events.models import Eevent, Einstance, Place

from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework import status

import logging


logger = logging.getLogger(__name__)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Eevent.objects.all()
    serializer_class = EeventSerializer
    renderer_classes = (JSONRenderer,)

    if settings.DEBUG:
        renderer_classes += (BrowsableAPIRenderer,)

    @list_route()
    def list(self, request):
        if request.method == 'GET':
            category = request.GET.get('category', '')
        queryset = self.queryset
        if category:
            queryset = queryset.filter(category_id=category)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def retrieve(self, request, pk=None):

        eevent = get_object_or_404(self.queryset, pk=pk)
        serializer = EeventSerializer(eevent,
                                      context={'request': request})
        return Response(serializer.data)

    # def crea_te(self, request):
    #     data = request.DATA
    #     event = Eevent()
    #     serializer = EeventSerializer(event, data=data)
    #     serializer.is_valid()
    #     serializer.save()
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED,
    #                     headers=headers)

    def update(self, request, pk=None):
        eevent = self.queryset.get(pk=pk)

        serializer = EeventSerializer(eevent, data=request.DATA)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        eevent = self.queryset.get(pk=pk)

        serializer = EeventSerializer(eevent, data=request.DATA)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    @detail_route(methods=['post', 'delete'])
    def delete(self, request, pk=None):
        json = {
            'success': False,
        }
        eevent = None
        try:
            eevent = self.queryset.get(id=pk)
        except eevent.DoesNotExist:
            pass

        if eevent:
            json.update({'success': True})

        json_response = simplejson.dumps(json)

        return Response(json_response)


class EinstanceViewSet(viewsets.ModelViewSet):

    queryset = Einstance.objects.all()
    serializer_class = InstanceSerializer

    def pre_save(self, obj):
        obj.eevent = self.request.eevent


class GeoViewSet(viewsets.ModelViewSet):

    queryset = Eevent.objects.all()
    serializer_class = EeventSerializer

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            long = request.GET.get('long', '')
            lat = request.GET.get('lat', '')
            radius = request.GET.get('radius', '')
            places = []
            if long and lat and radius:
                for place in Place.objects.filter(lat__isnull=False,
                                                  long__isnull=False):
                    km = great_circle((lat, long), (place.lat, place.long))
                    if int(radius) <= km.kilometers:
                        places.append(place)

        event_ids = tuple(inst.eevent_id for inst in Einstance.objects.filter(
            place__in=places))

        queryset = Eevent.objects.filter(id__in=event_ids)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass
