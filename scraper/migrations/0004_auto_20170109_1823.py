# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-09 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=10)),
                ('mileage', models.CharField(max_length=6)),
                ('body_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.BodyType')),
            ],
        ),
        migrations.CreateModel(
            name='CarName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.RenameField(
            model_name='year',
            old_name='text',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='year',
            name='value',
        ),
        migrations.AddField(
            model_name='car',
            name='car_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.CarName'),
        ),
        migrations.AddField(
            model_name='car',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.Year'),
        ),
    ]