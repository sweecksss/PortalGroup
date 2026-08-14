from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'starts_at', 'ends_at', 'location', 'author')
    list_filter = ('starts_at', 'author')
    search_fields = ('title', 'description', 'location', 'author__username')
    date_hierarchy = 'starts_at'
    ordering = ('-starts_at',)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
