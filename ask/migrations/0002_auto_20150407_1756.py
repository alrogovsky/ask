# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.CharField(max_length=30)),
                ('string_long', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='string_long',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
