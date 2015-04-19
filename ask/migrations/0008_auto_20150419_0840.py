# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0007_auto_20150419_0839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='user_id',
            new_name='user',
        ),
    ]
