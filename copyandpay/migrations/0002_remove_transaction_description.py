# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 20:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copyandpay', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='description',
        ),
    ]
