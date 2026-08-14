from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Назва події')),
                ('description', models.TextField(verbose_name='Опис')),
                ('starts_at', models.DateTimeField(verbose_name='Початок')),
                ('ends_at', models.DateTimeField(blank=True, null=True, verbose_name='Завершення')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='Місце проведення')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['starts_at']},
        ),
    ]
