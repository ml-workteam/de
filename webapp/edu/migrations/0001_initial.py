# Generated by Django 3.1.6 on 2021-02-12 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('is_guest', models.SmallIntegerField(choices=[(0, 'Guest'), (1, 'Registered')], default=0)),
                ('registration_date', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0))),
                ('join_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('join_date',),
            },
        ),
    ]
