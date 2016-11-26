# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-26 21:53
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('drip', '0004_auto_20161126_1653'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=75)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('drip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sendgrid_events', to='drip.Drip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sendgrid_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
        ),
    ]
