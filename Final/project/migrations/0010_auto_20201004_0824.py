# Generated by Django 3.1 on 2020-10-04 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20201004_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='/media/pictures/default.jpg', upload_to='pictures'),
        ),
    ]