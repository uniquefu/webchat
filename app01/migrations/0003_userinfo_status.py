# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-14 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20180313_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='status',
            field=models.IntegerField(choices=[(0, '在线'), (1, '隐身'), (2, '离开'), (3, '忙碌')], default=0),
        ),
    ]
