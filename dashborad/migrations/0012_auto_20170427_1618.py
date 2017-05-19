# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0011_auto_20170427_1159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idc',
            old_name='address',
            new_name='idc_address',
        ),
        migrations.RenameField(
            model_name='idc',
            old_name='user',
            new_name='idc_user',
        ),
    ]
