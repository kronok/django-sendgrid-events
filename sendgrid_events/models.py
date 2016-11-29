import json
import logging
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from pytz import AmbiguousTimeError

from .signals import batch_processed
from drip.models import Drip

logger = logging.getLogger(__name__)


class Event(models.Model):
    kind = models.CharField(max_length=75)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sendgrid_events')
    drip = models.ForeignKey('drip.Drip', related_name='sendgrid_events', blank=True, null=True)
    data = JSONField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        get_latest_by = "created_at"
        app_label = "sendgrid_events"

    @classmethod
    def process_batch(cls, data):
        User = get_user_model()
        events = []
        for event in json.loads(data):
            try:
                drip_pk = event.get("drip_pk", None)
                user_pk = event.get("user_pk", None)
                user = User.objects.get(pk=user_pk)
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
                    #created_at=timezone.get_current_timezone().localize(timezone.datetime.fromtimestamp(event["timestamp"]), is_dst=False)

                ))
            except User.DoesNotExist:
                msg = 'User email %s not found' % (event["email"])
                logger.error(msg)
            except Drip.DoesNotExist:
                msg = 'Drip %s not found' % (str(drip_pk))
                logger.error(msg)
            except AmbiguousTimeError:
                msg = 'Bad time found. Possible daylight savings time problem.'
                logger.error(msg)
        if events:
            batch_processed.send(sender=Event, events=events)
        return events