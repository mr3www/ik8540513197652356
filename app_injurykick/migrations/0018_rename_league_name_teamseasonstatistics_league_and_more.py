# Generated by Django 5.1.1 on 2024-10-09 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0017_rename_league_id_teamseasonstatistics_league_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teamseasonstatistics',
            old_name='league_name',
            new_name='league',
        ),
        migrations.RenameField(
            model_name='teamseasonstatistics',
            old_name='team_name',
            new_name='team',
        ),
    ]