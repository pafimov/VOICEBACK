# Generated by Django 3.2.5 on 2023-05-30 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_word_video_word_word_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='accent',
            field=models.CharField(default='British', max_length=100),
        ),
    ]
