from django.urls import path

from . import views

app_name = 'votings'

urlpatterns = [
    path('', views.voting_list, name='list'),
    path('create/', views.create_voting, name='create'),
    path('<int:pk>/', views.voting_detail, name='detail'),
    path('<int:pk>/vote/', views.cast_vote, name='vote'),
    path('<int:pk>/toggle/', views.toggle_voting, name='toggle'),
]
