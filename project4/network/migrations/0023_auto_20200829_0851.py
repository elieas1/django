# Generated by Django 3.1 on 2020-08-29 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0022_auto_20200829_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='followeduser',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='following',
            name='followinguser',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 29, 8, 51, 24, 521353)),
        ),
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.TextField(default=''),
        ),
    ]
