from celery import task

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from sendgrid_events.models import Event
from sendgrid_events.tasks import event_process_batch_task


@require_POST
@csrf_exempt
def handle_batch_post(request):
    if settings.SENDGRIDEVENTS_USE_CELERY:
        event_process_batch_task.delay(request.body)
    else:
        Event.process_batch(data=request.body)
    return HttpResponse()