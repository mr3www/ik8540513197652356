# Generated by Django 5.1.1 on 2024-10-30 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0018_fixtureplayerstatistics_offsides'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixtureplayerstatistics',
            name='substitute',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
