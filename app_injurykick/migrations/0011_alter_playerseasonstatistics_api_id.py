# Generated by Django 5.1.1 on 2024-10-13 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0010_remove_player_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerseasonstatistics',
            name='api_id',
            field=models.IntegerField(),
        ),
    ]
