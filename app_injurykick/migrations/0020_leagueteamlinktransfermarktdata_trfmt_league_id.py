# Generated by Django 5.1.1 on 2024-10-13 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0019_leagueteamlinktransfermarktdata_trfmt_team_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='leagueteamlinktransfermarktdata',
            name='trfmt_league_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
