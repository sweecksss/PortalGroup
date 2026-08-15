from django.contrib import admin
from .models import Album, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'description')
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('album', 'caption', 'uploaded_by', 'uploaded_at', 'is_approved')
    list_filter = ('is_approved', 'uploaded_at', 'album')
    search_fields = ('caption',)
    actions = ['approve_selected']

    @admin.action(description='Схвалити вибрані файли')
    def approve_selected(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'Схвалено файлів: {updated}.')
