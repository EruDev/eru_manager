# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-06-12 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CmdList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmd', models.CharField(max_length=128, verbose_name='命令')),
                ('host', models.CharField(default='192.168.43.214 ', max_length=128, verbose_name='主机')),
                ('time', models.DateTimeField(verbose_name='发出命令的时间')),
            ],
        ),
    ]
