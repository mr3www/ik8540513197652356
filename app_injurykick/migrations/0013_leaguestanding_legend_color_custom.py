# Generated by Django 5.1.1 on 2024-10-13 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0012_leaguestanding_legend_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaguestanding',
            name='legend_color_custom',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
