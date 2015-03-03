import json
import logging

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from jsonfield import JSONField #see what djstripe does

from sendgrid_events.signals import batch_processed
from drip.models import Drip

logger = logging.getLogger(__name__)


class Event(models.Model):
    kind = models.CharField(max_length=75)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sendgrid_events')
    drip = models.ForeignKey('drip.Drip', related_name='sendgrid_events', blank=True, null=True)
    data = JSONField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        get_latest_by = "created_at" #this isn't right

    @classmethod
    def process_batch(cls, data):
        User = get_user_model()
        events = []
        for event in json.loads(data):
            try:
                drip_pk = event.get("drip_pk", None)
                user_pk = event.get("user_pk", None)
                user = User.objects.get(pk=user_pk)
                #user = User.objects.get(email=event["email"])
                #user = User.objects.get(email='angelasciarappa@gmail.com')
                drip = None
                if drip_pk:
                    drip_pk = int(drip_pk)
                    drip = Drip.objects.get(pk=drip_pk)
                events.append(Event.objects.create(
                    kind=event["event"],
                    user=user,
                    drip=drip,
                    data=event,
                    created_at=timezone.datetime.fromtimestamp(event["timestamp"])
                ))
            except User.DoesNotExist:
                msg = 'User email %s not found' % (event["email"])
                logger.error(msg)
            except Drip.DoesNotExist:
                #couldn't get a drip_pk
                msg = 'Drip %s not found' % (str(drip_pk))
                logger.error(msg)
        if events:
            batch_processed.send(sender=Event, events=events)
        return events

"""
class DripEvent(models.Model):
    drip = models.ForeignKey('drip.Drip', related_name="email_events")
    sendgrid_event = models.ForeignKey(Event, related_name="+")

    class Meta:
        ordering = ["sendgrid_event__created_at"]

@receiver(batch_processed)
def handle_batch_processed(sender, events, **kwargs):
    for event in events:
        try:
            #extract drip_pk from event and create a DripEvent for it
            drip_pk = event.data['unique_args'].get('drip_pk', None)
            c = Drip.objects.get(pk=drip_pk)
            c.email_events.create(sendgrid_event=event)
        except Drip.DoesNotExist:
            #couldn't get a drip_pk
            msg = 'Drip %s not found' % (str(drip_pk))
            logger.error(msg)
        except KeyError:
            #it's having an issue with the unique_args not being passed in, which means it's pointless to record atm
            msg = 'No unique_args found in sendgrid email'
            logger.error(msg)
"""