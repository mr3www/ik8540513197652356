# Generated by Django 5.1.1 on 2024-11-01 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0021_remove_leaguestanding_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='leaguestanding',
            unique_together=set(),
        ),
    ]
