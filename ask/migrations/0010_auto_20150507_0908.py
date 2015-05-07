# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0009_auto_20150425_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar_url',
            field=models.ImageField(default=b'/no-ava.jpg', upload_to=b'/avatars'),
        ),
    ]
