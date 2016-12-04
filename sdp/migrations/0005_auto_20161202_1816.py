# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 10:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sdp', '0004_auto_20161127_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component_Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sequence', models.PositiveIntegerField()),
                ('component_type', models.CharField(choices=[('T', 'Text'), ('F', 'File'), ('I', 'Image'), ('V', 'VIDEO')], default='T', max_length=1)),
                ('file_field', embed_video.fields.EmbedVideoField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdp.Module')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='component_file',
            name='component_type',
            field=models.CharField(choices=[('T', 'Text'), ('F', 'File'), ('I', 'Image'), ('V', 'VIDEO')], default='T', max_length=1),
        ),
        migrations.AlterField(
            model_name='component_image',
            name='component_type',
            field=models.CharField(choices=[('T', 'Text'), ('F', 'File'), ('I', 'Image'), ('V', 'VIDEO')], default='T', max_length=1),
        ),
        migrations.AlterField(
            model_name='component_text',
            name='component_type',
            field=models.CharField(choices=[('T', 'Text'), ('F', 'File'), ('I', 'Image'), ('V', 'VIDEO')], default='T', max_length=1),
        ),
    ]
