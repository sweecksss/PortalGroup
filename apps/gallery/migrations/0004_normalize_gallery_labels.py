from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('gallery', '0003_photo_image_to_file')]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['-created_at'], 'verbose_name': 'Альбом', 'verbose_name_plural': 'Альбоми'},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-uploaded_at'], 'verbose_name': 'Файл альбому', 'verbose_name_plural': 'Файли альбому'},
        ),
        migrations.AlterField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата створення'),
        ),
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True, verbose_name='Опис альбому'),
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Назва альбому'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='caption',
            field=models.CharField(blank=True, max_length=255, verbose_name='Підпис'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата завантаження'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Завантажив'),
        ),
    ]
