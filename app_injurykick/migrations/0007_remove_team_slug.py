# Generated by Django 5.1.1 on 2024-10-07 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0006_leaguestanding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='slug',
        ),
    ]
