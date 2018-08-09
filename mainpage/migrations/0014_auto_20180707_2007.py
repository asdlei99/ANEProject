# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-07 20:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0013_animals_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='images',
            name='types',
        ),
        migrations.AddField(
            model_name='images',
            name='animalOwner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AnimalImage', to='mainpage.Animals'),
        ),
        migrations.AddField(
            model_name='images',
            name='bookOwner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BookImage', to='mainpage.Book'),
        ),
        migrations.AddField(
            model_name='images',
            name='shopOwner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ShopImage', to='mainpage.Food'),
        ),
    ]