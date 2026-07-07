# core/migrations/0002_add_publisher_and_media_type.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='book',
            name='media_type',
            field=models.CharField(
                choices=[
                    ('book', 'Book'),
                    ('cd', 'CD'),
                    ('dvd', 'DVD'),
                    ('magazine', 'Magazine'),
                    ('audiobook', 'Audiobook'),
                ],
                default='book',
                max_length=20,
            ),
        ),
    ]