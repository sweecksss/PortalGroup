from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):
    title = models.CharField('Назва події', max_length=200)
    description = models.TextField('Опис')
    starts_at = models.DateTimeField('Початок')
    ends_at = models.DateTimeField('Завершення', blank=True, null=True)
    location = models.CharField('Місце проведення', max_length=255, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='events', verbose_name='Автор')
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        verbose_name = 'Подія'
        verbose_name_plural = 'Події'
        ordering = ['starts_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    @property
    def start_date(self):
        """Дата початку в локальному часовому поясі."""
        return timezone.localtime(self.starts_at).date()

    @property
    def end_date(self):
        """Дата завершення (для подій без кінця — це день початку)."""
        if self.ends_at:
            return timezone.localtime(self.ends_at).date()
        return self.start_date

    @property
    def is_past(self):
        return (self.ends_at or self.starts_at) < timezone.now()

    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.starts_at <= now and (self.ends_at or self.starts_at) >= now
