# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(blank=True, verbose_name='name', max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(blank=True, verbose_name='name', max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'cities',
                'verbose_name': 'city',
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Eevent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', blank=True, default='', max_length=255, null=True)),
                ('description', models.TextField(help_text='Event Description', verbose_name='description', blank=True, null=True)),
                ('category', models.ForeignKey(to='events.Category', blank=True, verbose_name='category', null=True)),
            ],
            options={
                'verbose_name_plural': 'events',
                'verbose_name': 'event',
                'db_table': 'eevent',
            },
        ),
        migrations.CreateModel(
            name='Einstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('start', models.DateTimeField(verbose_name='start', blank=True, default=django.utils.timezone.now, null=True)),
                ('end', models.DateTimeField(verbose_name='end', blank=True, default=django.utils.timezone.now, null=True)),
                ('eevent', models.ForeignKey(related_name='instances', to='events.Eevent')),
            ],
            options={
                'verbose_name_plural': 'instances',
                'verbose_name': 'instance',
                'db_table': 'einstance',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(blank=True, verbose_name='name', max_length=255, null=True)),
                ('long', models.FloatField(blank=True, verbose_name='longitude', null=True)),
                ('lat', models.FloatField(blank=True, verbose_name='latitude', null=True)),
                ('city', models.ForeignKey(verbose_name='city', to='events.City')),
            ],
            options={
                'verbose_name_plural': 'places',
                'verbose_name': 'place',
                'db_table': 'place',
            },
        ),
        migrations.AddField(
            model_name='einstance',
            name='place',
            field=models.ForeignKey(verbose_name='place', to='events.Place'),
        ),
    ]
