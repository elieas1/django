# Generated by Django 3.1.6 on 2021-02-18 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
