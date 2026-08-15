from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()

class PortfolioModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project = Project.objects.create(
            title='Тестовий проект',
            description='Опис тестового проекта',
            author=self.user
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, 'Тестовий проект')
        self.assertEqual(str(self.project), 'Тестовий проект')
