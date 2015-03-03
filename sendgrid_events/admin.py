from django.contrib import admin

from .models import Event


admin.site.register(Event, list_display=["kind", "user", "drip", "created_at"], list_filter=["created_at", "kind"], search_fields=["user", "data"], raw_id_fields = ['user', 'drip'])
