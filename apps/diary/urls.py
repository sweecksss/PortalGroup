from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.DiaryOverviewView.as_view(), name='overview'),
    path('student/<int:pk>/', views.StudentGradesView.as_view(), name='student_detail'),
]
