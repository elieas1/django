# Generated by Django 3.1 on 2020-08-29 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_auto_20200829_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='followeduser',
            field=models.TextField(default='...'),
        ),
        migrations.AlterField(
            model_name='following',
            name='followinguser',
            field=models.TextField(default='...'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 29, 8, 12, 29, 379462)),
        ),
    ]
