from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('calendar/', views.EventCalendarView.as_view(), name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.EventCalendarView.as_view(), name='calendar_month'),
    path('calendar/<int:year>/<int:month>/<int:day>/', views.EventDayView.as_view(), name='day'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete'),
]
