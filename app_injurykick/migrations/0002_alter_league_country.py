# Generated by Django 5.1.1 on 2024-10-07 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
