# Generated by Django 3.1 on 2020-12-08 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unesco', '0002_auto_20201208_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='area_hectares',
            field=models.FloatField(null=True),
        ),
    ]