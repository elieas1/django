# Generated by Django 3.1 on 2020-08-30 11:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0027_auto_20200830_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='like',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likedpost', to='network.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 30, 4, 32, 17, 293904)),
        ),
    ]
