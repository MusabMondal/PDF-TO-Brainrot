# Generated by Django 5.0.9 on 2024-11-27 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_processor', '0002_pdf_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='audios/'),
        ),
        migrations.AddField(
            model_name='pdf',
            name='summary',
            field=models.TextField(blank=True),
        ),
    ]
