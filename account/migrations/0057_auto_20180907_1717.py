# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-07 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0056_auto_20180907_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='nickname',
            field=models.CharField(default='WHUer570063', max_length=20, verbose_name='nickname'),
        ),
    ]
