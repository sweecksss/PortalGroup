from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('create/', views.album_create, name='album_create'),
    path('<int:pk>/', views.album_detail, name='album_detail'),
    path('<int:album_pk>/upload/', views.photo_upload, name='photo_upload'),
    path('photo/<int:pk>/approve/', views.photo_approve, name='photo_approve'),
    path('photo/<int:pk>/delete/', views.photo_delete, name='photo_delete'),
]
