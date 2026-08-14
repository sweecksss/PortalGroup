from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('gallery', '0002_alter_album_options_alter_photo_options_and_more')]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.FileField(upload_to='gallery/', verbose_name='Файл'),
        ),
    ]
