from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'file', 'link', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'link', 'author__username')
