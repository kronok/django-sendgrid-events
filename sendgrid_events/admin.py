from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display=["kind", "user", "drip", "created_at"]
    list_filter=["created_at", "kind"]
    search_fields=["user__email", "user__username", "data", "drip__name"]
    raw_id_fields = ['user', 'drip']

admin.site.register(Event, EventAdmin)
