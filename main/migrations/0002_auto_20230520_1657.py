# Generated by Django 3.2.5 on 2023-05-20 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='sentece_video',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='word_video',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]