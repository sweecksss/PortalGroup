from django.db import models
from django.conf import settings

IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg')
VIDEO_EXTENSIONS = ('mp4', 'webm', 'ogg', 'mov', 'm4v')


class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва альбому")
    description = models.TextField(blank=True, verbose_name="Опис альбому")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="albums",
        verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбоми"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Альбом"
    )
    image = models.FileField(upload_to="gallery/", verbose_name="Файл")
    caption = models.CharField(max_length=255, blank=True, verbose_name="Підпис")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата завантаження")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Завантажив"
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Схвалено",
        help_text="Файл показується в галереї лише після перевірки модератором.",
    )

    class Meta:
        verbose_name = "Файл альбому"
        verbose_name_plural = "Файли альбому"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Файл в альбомі '{self.album.title}' ({self.caption or 'Без назви'})"

    @property
    def extension(self):
        return self.image.name.rsplit('.', 1)[-1].lower() if '.' in self.image.name else ''

    @property
    def is_image(self):
        return self.extension in IMAGE_EXTENSIONS

    @property
    def is_video(self):
        return self.extension in VIDEO_EXTENSIONS
