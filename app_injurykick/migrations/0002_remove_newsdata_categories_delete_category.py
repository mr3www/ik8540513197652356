# Generated by Django 5.1.1 on 2024-10-16 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_injurykick', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsdata',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
