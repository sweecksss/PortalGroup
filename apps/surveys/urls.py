from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.survey_list, name='list'),
    path('<int:survey_id>/start/', views.start_survey, name='start'),
    path('<int:survey_id>/question/', views.question_view, name='question'),
    path('<int:survey_id>/thanks/', views.thanks_view, name='thanks'),
    path('<int:survey_id>/results/', views.results_view, name='results'),
]
