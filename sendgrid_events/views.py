from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from .models import Event
from .tasks import event_process_batch_task


@require_POST
@csrf_exempt
def handle_batch_post(request):
    if getattr(settings, 'SENDGRIDEVENTS_USE_CELERY', False):
        event_process_batch_task.delay(request.body)
    else:
        Event.process_batch(data=request.body)
    return HttpResponse()
