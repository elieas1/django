# Generated by Django 3.1.6 on 2021-02-24 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210224_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnail'),
        ),
    ]