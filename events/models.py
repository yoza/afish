"""
Events app models
"""
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from geopy.geocoders import GoogleV3


class CategoryManager(models.Manager):
    pass


class Category(models.Model):
    """
    Category model

    """
    name = models.CharField(_('name'), max_length=255, null=True, blank=True,
                            default='', help_text=_('Category Name'))

    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('name',)
        db_table = 'category'
        app_label = 'events'

    def __str__(self):
        return self.name


class CityManager(models.Manager):
    pass


class City(models.Model):
    """
    City model

    """
    name = models.CharField(_('name'), max_length=255, null=True, blank=True,
                            default='', help_text=_('City Name'))

    objects = CityManager()

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        ordering = ('name',)
        db_table = 'city'
        app_label = 'events'

    def __str__(self):
        return self.name


class PlaceManager(models.Manager):

    @classmethod
    def geoaddr(cls, addr):
        geolocator = GoogleV3()
        return geolocator.geocode(addr)


class Place(models.Model):
    """
    Place model

    """
    name = models.CharField(_('name'), max_length=255, null=True, blank=True,
                            default='',
                            help_text=_('Place Name'))
    long = models.FloatField(_('longitude'), blank=True, null=True)
    lat = models.FloatField(_('latitude'), blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)

    objects = PlaceManager()

    class Meta:
        verbose_name = _('place')
        verbose_name_plural = _('places')
        ordering = ('city__name', 'name')
        db_table = 'place'
        app_label = 'events'

    def save(self, *args, **kwargs):
        """ save method """
        geo = Place.objects.geoaddr(self.name + self.city.name)
        if geo:
            _, geocode = geo
            self.long = geocode[1]
            self.lat = geocode[0]
        super(Place, self).save(*args, **kwargs)
    save.alters_data = True

    def __str__(self):
        return "%s - %s" % (self.city.name, self.name)


class EeventManager(models.Manager):
    pass


class Eevent(models.Model):
    """
    Event model

    """
    title = models.CharField(_('title'), max_length=255, null=True, blank=True,
                             default='', help_text=_('Event Name'))
    description = models.TextField(_('description'), null=True, blank=True,
                                   help_text=_('Event Description'))
    category = models.ForeignKey('Category', blank=True, null=True,
                                 verbose_name=_('category'))

    objects = EeventManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title',)
        db_table = 'eevent'
        app_label = 'events'

    def __str__(self):
        return self.title


class EinstanceManager(models.Manager):
    pass


class Einstance(models.Model):
    """
    Instance model

    """
    start = models.DateTimeField(_('start date'),
                                 default=timezone.now)
    end = models.DateTimeField(_('stop date'), null=True, blank=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    eevent = models.ForeignKey(Eevent, verbose_name=_('event'),
                               blank=True, null=True, related_name='instances')
    objects = EinstanceManager()

    class Meta:
        verbose_name = _('instance')
        verbose_name_plural = _('instances')
        ordering = ('start',)
        db_table = 'einstance'
        app_label = 'events'


class EventManager(models.Manager):
    pass
