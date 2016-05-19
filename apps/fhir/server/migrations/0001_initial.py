# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-18 04:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceTypeControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('override_url_id', models.BooleanField(help_text='Does this resource need to mask the id in the url?')),
                ('override_search', models.BooleanField(help_text="Do search parameters need to be filtered to avoid revealing other people's data?")),
                ('search_block', models.TextField(default='', help_text='list of values that need to be removed from search parameters. eg. Patient', max_length=5120)),
                ('search_add', models.TextField(default='', help_text='list of keys that need to be added tosearch parameters to filter informationthat is returned. eg. Patient.', max_length=200)),
                ('group_allow', models.TextField(default='', help_text='groups permitted to access resource.', max_length=100)),
                ('group_exclude', models.TextField(default='', help_text='groups blocked from accessing resource.', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SupportedResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_name', models.CharField(db_index=True, max_length=256, unique=True)),
                ('json_schema', models.TextField(default='{}', help_text='{} indicates no schema.', max_length=5120)),
                ('get', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='get')),
                ('put', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='put')),
                ('create', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='create')),
                ('read', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='read')),
                ('vread', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='vread')),
                ('update', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='update')),
                ('delete', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='delete')),
                ('search', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='search')),
                ('history', models.BooleanField(default=False, help_text='FHIR Interaction Type', verbose_name='_history')),
            ],
        ),
        migrations.AddField(
            model_name='resourcetypecontrol',
            name='resource_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.SupportedResourceType'),
        ),
    ]
