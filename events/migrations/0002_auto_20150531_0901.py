# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('name',), 'verbose_name': 'city', 'verbose_name_plural': 'cities'},
        ),
        migrations.AlterModelOptions(
            name='eevent',
            options={'ordering': ('title',), 'verbose_name': 'event', 'verbose_name_plural': 'events'},
        ),
        migrations.AlterModelOptions(
            name='einstance',
            options={'ordering': ('start',), 'verbose_name': 'instance', 'verbose_name_plural': 'instances'},
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'ordering': ('city__name', 'name'), 'verbose_name': 'place', 'verbose_name_plural': 'places'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='', null=True, verbose_name='name', blank=True, help_text='Category Name', max_length=255),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(default='', null=True, verbose_name='name', blank=True, help_text='City Name', max_length=255),
        ),
        migrations.AlterField(
            model_name='eevent',
            name='title',
            field=models.CharField(default='', null=True, verbose_name='title', blank=True, help_text='Event Name', max_length=255),
        ),
        migrations.AlterField(
            model_name='einstance',
            name='eevent',
            field=models.ForeignKey(null=True, related_name='instances', verbose_name='event', blank=True, to='events.Eevent'),
        ),
        migrations.AlterField(
            model_name='einstance',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='stop date', blank=True),
        ),
        migrations.AlterField(
            model_name='einstance',
            name='place',
            field=models.ForeignKey(null=True, to='events.Place', blank=True),
        ),
        migrations.AlterField(
            model_name='einstance',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='place',
            name='city',
            field=models.ForeignKey(null=True, to='events.City', blank=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(default='', null=True, verbose_name='name', blank=True, help_text='Place Name', max_length=255),
        ),
    ]
