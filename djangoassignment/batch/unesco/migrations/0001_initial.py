# Generated by Django 3.1 on 2020-12-08 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Iso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('year', models.IntegerField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unesco.category')),
                ('site-iso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unesco.iso')),
                ('site-region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unesco.region')),
                ('site-state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unesco.state')),
            ],
        ),
    ]
