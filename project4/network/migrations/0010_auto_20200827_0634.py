# Generated by Django 3.1 on 2020-08-27 13:34

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20200826_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userfollows',
            field=models.ManyToManyField(blank=True, related_name='_user_userfollows_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 6, 34, 30, 659932)),
        ),
    ]
