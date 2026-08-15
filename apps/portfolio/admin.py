from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'technologies', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'description', 'technologies')
