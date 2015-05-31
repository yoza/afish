from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from geopy.geocoders import GoogleV3


class CategoryManager(models.Manager):
    pass


class Category(models.Model):

    name = models.CharField(_('name'), max_length=255, null=True, blank=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'category'
        app_label = 'events'

    def __str__(self):
        return self.name


class CityManager(models.Manager):
    pass


class City(models.Model):

    name = models.CharField(_('name'), max_length=255, null=True, blank=True)

    objects = CityManager()

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        db_table = 'city'
        app_label = 'events'

    def __str__(self):
        return self.name


class PlaceManager(models.Manager):
    pass


class Place(models.Model):

    name = models.CharField(_('name'), max_length=255, null=True, blank=True)
    long = models.FloatField(_('longitude'), blank=True, null=True)
    lat = models.FloatField(_('latitude'), blank=True, null=True)
    city = models.ForeignKey(City, verbose_name=_("city"))
    objects = PlaceManager()

    class Meta:
        verbose_name = _('place')
        verbose_name_plural = _('places')
        db_table = 'place'
        app_label = 'events'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """  save method """
        geolocator = GoogleV3()
        geocodes = geolocator.geocode(self.name + self.city.name)
        if geocodes:
            _, (self.lat, self.long) = geocodes
        super(Place, self).save(*args, **kwargs)
    save.alters_data = True


class EeventManager(models.Manager):
    pass


class Eevent(models.Model):

    title = models.CharField(_('title'), max_length=255, null=True, blank=True,
                             default='')
    description = models.TextField(_('description'), null=True, blank=True,
                                   help_text=_('Event Description'))
    category = models.ForeignKey(Category, verbose_name=_("category"),
                                 null=True, blank=True)
    objects = EeventManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        db_table = 'eevent'
        app_label = 'events'

    def __str__(self):
        return self.title


class EinstanceManager(models.Manager):
    pass


class Einstance(models.Model):

    start = models.DateTimeField(_('start'), null=True, blank=True,
                                 default=timezone.now)
    end = models.DateTimeField(_('end'), null=True, blank=True,
                               default=timezone.now)

    place = models.ForeignKey(Place, verbose_name=_("place"))
    eevent = models.ForeignKey(Eevent, related_name='instances')

    objects = EinstanceManager()

    class Meta:
        verbose_name = _('instance')
        verbose_name_plural = _('instances')
        db_table = 'einstance'
        app_label = 'events'

    def __str__(self):
        return self.eevent.title
