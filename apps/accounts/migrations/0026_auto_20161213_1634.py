# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-13 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_userprofile_authorize_applications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistercode',
            name='resend',
            field=models.BooleanField(default=False, help_text='Check to resend'),
        ),
    ]
