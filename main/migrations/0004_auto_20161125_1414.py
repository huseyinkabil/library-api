# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20161125_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]