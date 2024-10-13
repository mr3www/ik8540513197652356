# Generated by Django 5.1.1 on 2024-10-13 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0016_league_country_code_custom_alter_league_country_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueTeamLinkTransfermarktData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('league', models.CharField(blank=True, max_length=255, null=True)),
                ('season', models.IntegerField(blank=True, null=True)),
                ('team', models.CharField(blank=True, max_length=255, null=True)),
                ('link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerTransfermarktData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('league', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('team', models.CharField(blank=True, max_length=255, null=True)),
                ('position', models.CharField(blank=True, max_length=100, null=True)),
                ('number', models.CharField(blank=True, max_length=10, null=True)),
                ('market_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('market_value_cleaned', models.CharField(max_length=255)),
                ('market_value_transformed', models.CharField(max_length=255)),
                ('image', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
