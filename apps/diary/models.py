from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StudentProfile(models.Model):
    """Профіль учня — розширення користувача даними, потрібними для щоденника."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Користувач',
    )
    school_class = models.CharField(
        max_length=20,
        verbose_name='Клас',
        help_text='Наприклад: 10-А',
    )

    class Meta:
        verbose_name = 'Профіль учня'
        verbose_name_plural = 'Профілі учнів'
        ordering = ['school_class', 'user__last_name', 'user__first_name']

    def __str__(self):
        full_name = self.user.get_full_name() or self.user.username
        return f'{full_name} ({self.school_class})'


class Subject(models.Model):
    """Навчальний предмет."""
    name = models.CharField(max_length=100, unique=True, verbose_name='Назва предмета')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предмети'
        ordering = ['name']

    def __str__(self):
        return self.name


class Grade(models.Model):
    """Оцінка учня з певного предмета (12-бальна шкала)."""
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Учень',
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Предмет',
    )
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='Оцінка',
        help_text='За 12-бальною шкалою',
    )
    date_given = models.DateField(auto_now_add=True, verbose_name='Дата виставлення')
    given_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='given_grades',
        verbose_name='Виставив',
    )

    class Meta:
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'
        ordering = ['-date_given']

    def __str__(self):
        return f'{self.student} - {self.subject}: {self.value}'
