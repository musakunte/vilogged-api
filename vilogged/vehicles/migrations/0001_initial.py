# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-11 06:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('_rev', models.CharField(editable=False, max_length=100, unique=True)),
                ('license', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('vehicle_type', models.CharField(blank=True, max_length=50, null=True)),
                ('color', models.CharField(blank=True, max_length=20, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('appointment_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to='appointments.Appointments')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ve_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ve_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
