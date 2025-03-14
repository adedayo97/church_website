# Generated by Django 5.1.6 on 2025-03-08 17:39

import church.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageupload',
            name='category',
            field=models.CharField(choices=[('service', 'Service'), ('gallery', 'Gallery'), ('pastor', 'Pastor'), ('event', 'Event'), ('hero', 'Hero')], default='gallery', max_length=20),
        ),
        migrations.AddField(
            model_name='imageupload',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='imageupload',
            name='description',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imageupload',
            name='image',
            field=models.ImageField(upload_to=church.models.upload_to_path),
        ),
    ]
