# Generated by Django 5.1.1 on 2024-11-03 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0025_alter_sidelined_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='away_next',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='home_next',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]