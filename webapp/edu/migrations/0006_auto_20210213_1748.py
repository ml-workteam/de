# Generated by Django 3.1.6 on 2021-02-13 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0005_auto_20210213_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
