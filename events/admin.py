"""
site admin registers
"""
from django.contrib import admin
from events import models


class CategoryAdmin(admin.ModelAdmin):
    actions_on_top = False
    actions_on_bottom = True

admin.site.register(models.Category, CategoryAdmin)


class CityAdmin(admin.ModelAdmin):
    actions_on_top = False
    actions_on_bottom = True

admin.site.register(models.City, CityAdmin)


class PlaceAdmin(admin.ModelAdmin):
    actions_on_top = False
    actions_on_bottom = True

    def get_readonly_fields(self, request, obj=None):
        """
        readonly fields
        """
        return tuple(field.name for field in self.model._meta.fields
                     if field.name in ['long', 'lat'])


admin.site.register(models.Place, PlaceAdmin)


class EinstanceInline(admin.StackedInline):
    actions_on_top = False
    actions_on_bottom = True
    model = models.Einstance


class EeventAdmin(admin.ModelAdmin):
    actions_on_top = False
    actions_on_bottom = True
    inlines = [EinstanceInline]

admin.site.register(models.Eevent, EeventAdmin)
