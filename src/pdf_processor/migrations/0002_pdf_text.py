# Generated by Django 5.0.9 on 2024-11-27 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_processor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
