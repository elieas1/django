# Generated by Django 3.1 on 2020-08-29 15:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_auto_20200829_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='followeduser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followeduser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='following',
            name='followinguser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followinguser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 29, 8, 13, 29, 801956)),
        ),
    ]
