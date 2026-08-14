from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.views import generic

from .models import StudentProfile, Subject, Grade


class DiaryOverviewView(LoginRequiredMixin, generic.TemplateView):
    """Загальна сторінка щоденника: зведена таблиця оцінок усіх учнів."""
    template_name = 'diary/overview.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subjects = list(Subject.objects.all())
        students = StudentProfile.objects.select_related('user')

        averages = {
            (row['student_id'], row['subject_id']): row['avg']
            for row in Grade.objects.values('student_id', 'subject_id').annotate(avg=Avg('value'))
        }

        table = []
        for student in students:
            row_grades = [averages.get((student.id, subject.id)) for subject in subjects]
            table.append({'student': student, 'grades': row_grades})

        context['subjects'] = subjects
        context['table'] = table
        return context


class StudentGradesView(LoginRequiredMixin, generic.DetailView):
    """Детальна сторінка з усіма оцінками одного учня."""
    model = StudentProfile
    template_name = 'diary/student_detail.html'
    context_object_name = 'student'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = self.object.grades.select_related('subject', 'given_by')
        return context
