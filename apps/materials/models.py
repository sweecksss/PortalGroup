import re

from django.db import models
from django.conf import settings

YOUTUBE_PATTERN = re.compile(
    r'(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/)|youtu\.be/)([\w-]{11})'
)
IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg')
VIDEO_EXTENSIONS = ('mp4', 'webm', 'ogg', 'mov', 'm4v')
AUDIO_EXTENSIONS = ('mp3', 'wav', 'oga', 'm4a')


class Material(models.Model):
    title = models.CharField('Назва матеріалу', max_length=180)
    description = models.TextField('Опис', blank=True)
    file = models.FileField('Файл', upload_to='materials/%Y/%m/', blank=True)
    link = models.URLField('Посилання', blank=True,
                           help_text='Посилання на сайт або відео YouTube — відкриється прямо на сторінці.')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='materials', verbose_name='Автор')
    created_at = models.DateTimeField('Додано', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'Матеріал'
        verbose_name_plural = 'Матеріали'
        ordering = ['-created_at']

    @property
    def extension(self):
        return self.file.name.rsplit('.', 1)[-1].lower() if self.file and '.' in self.file.name else ''

    @property
    def youtube_id(self):
        """ID відео, якщо посилання веде на YouTube."""
        if not self.link:
            return ''
        match = YOUTUBE_PATTERN.search(self.link)
        return match.group(1) if match else ''

    @property
    def youtube_embed_url(self):
        return f'https://www.youtube.com/embed/{self.youtube_id}' if self.youtube_id else ''

    @property
    def is_image(self):
        return self.extension in IMAGE_EXTENSIONS

    @property
    def is_video(self):
        return self.extension in VIDEO_EXTENSIONS

    @property
    def is_audio(self):
        return self.extension in AUDIO_EXTENSIONS

    @property
    def is_pdf(self):
        return self.extension == 'pdf'

    @property
    def kind(self):
        """Коротка позначка типу матеріалу для списку."""
        if self.youtube_id:
            return 'youtube'
        if self.link and not self.file:
            return 'посилання'
        return self.extension or 'файл'

    def __str__(self):
        return self.title
