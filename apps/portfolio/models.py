from django.db import models
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва проекту")
    description = models.TextField(verbose_name="Опис проекту")
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True, verbose_name="Превью / Скриншот")
    link = models.URLField(blank=True, verbose_name="Ссилка на проект  або GitHub")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавлення")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекти"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
