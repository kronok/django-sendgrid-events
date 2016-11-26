# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('drip', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=75)),
                ('data', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('drip', models.ForeignKey(related_name='sendgrid_events', blank=True, to='drip.Drip', null=True)),
                ('user', models.ForeignKey(related_name='sendgrid_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
            bases=(models.Model,),
        ),
    ]
