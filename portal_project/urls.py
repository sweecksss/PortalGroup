from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/', include('apps.accounts.urls')),
    path('forum/', include('apps.forum.urls')),
    path('diary/', include('apps.diary.urls')),
    path('events/', include('apps.events.urls')),
    path('surveys/', include('apps.surveys.urls')),
    path('votings/', include('apps.votings.urls')),
    path('announcements/', include('apps.announcements.urls')),
    path('materials/', include('apps.materials.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('gallery/', include('apps.gallery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
