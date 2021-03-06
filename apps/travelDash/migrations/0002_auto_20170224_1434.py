# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 19:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loginReg', '0001_initial'),
        ('travelDash', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='description',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trip',
            name='destination',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='usertrip',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelDash.Trip'),
        ),
        migrations.AddField(
            model_name='usertrip',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loginReg.User'),
        ),
    ]
