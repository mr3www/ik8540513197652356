# Generated by Django 5.1.1 on 2024-10-13 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0018_leagueteamlinktransfermarktdata_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='leagueteamlinktransfermarktdata',
            name='trfmt_team_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]