from rest_framework import serializers
from events import models


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('id', 'name')


class PlaceSerializer(serializers.ModelSerializer):

    city = CitySerializer()

    class Meta:
        model = models.Place
        fields = ('id', 'name', 'long', 'lat', 'city')


class InstanceSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = models.Einstance
        fields = ('start', 'end', 'place')


class EeventSerializer(serializers.ModelSerializer):
    instances = InstanceSerializer(many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = models.Eevent
        fields = ('id', 'title', 'description', 'category', 'instances')

    # TODO: create save related instances and category and drop read_only

    def create(self, validated_data):
        instance_data = validated_data.pop('instances', [])
        eevent = models.Eevent.objects.create(**validated_data)
        for instance in instance_data:
            place = instance.pop('place', None)
            if place:
                city = place.pop('city', None)
                if city:
                    city = models.City.objects.create(**city)
                    place['city'] = city
                place = models.Place.objects.create(**place)
                instance['place'] = place

            models.Einstance.objects.create(eevent=eevent, **instance)
        return eevent

    def update(self, event, validated_data):
        event.title = validated_data.get('title', event.title)
        event.description = validated_data.get('description',
                                               event.description)

        if 'instances' in validated_data:
            instances = validated_data.pop('instances', [])

            current_instances = models.Einstance.objects.filter(
                eevent__pk=event.id)
            updated_ids = set()

            for instance in instances:
                instance_id = instance.get('id')
                if instance_id:
                    inst = models.Einstance.objects.get(pk=instance_id)
                    inst.update(**instance)
                    inst.save()
                    updated_ids.add(instance_id)
                else:
                    place = instance.pop('place', None)
                    if place:
                        city = place.pop('city', None)
                        if city:
                            city = models.City.objects.create(**city)
                            place['city'] = city
                        place = models.Place.objects.create(**place)
                        instance['place'] = place
                    models.Einstance.objects.create(eevent=event, **instance)

            for cur_inst in current_instances:
                if cur_inst.id not in updated_ids:
                    cur_inst.delete()

        event.save()

        return event
