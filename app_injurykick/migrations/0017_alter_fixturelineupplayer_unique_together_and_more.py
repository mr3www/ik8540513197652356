# Generated by Django 5.1.1 on 2024-10-30 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0016_alter_fixtureteamstatistics_value'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fixturelineupplayer',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='fixtureplayerstatistics',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='fixtureteamstatistics',
            unique_together=set(),
        ),
    ]
