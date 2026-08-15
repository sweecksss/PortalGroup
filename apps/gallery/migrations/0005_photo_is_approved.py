from django.db import migrations, models


def approve_existing_photos(apps, schema_editor):
    """Файли, завантажені до появи модерації, залишаються опублікованими."""
    Photo = apps.get_model('gallery', 'Photo')
    Photo.objects.update(is_approved=True)


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_normalize_gallery_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='is_approved',
            field=models.BooleanField(default=False, help_text='Файл показується в галереї лише після перевірки модератором.', verbose_name='Схвалено'),
        ),
        migrations.RunPython(approve_existing_photos, migrations.RunPython.noop),
    ]
