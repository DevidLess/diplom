# Generated by Django 3.1.3 on 2025-01-11 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0002_auto_20250111_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='lawyers/photos/', verbose_name='Фотография'),
        ),
    ]
