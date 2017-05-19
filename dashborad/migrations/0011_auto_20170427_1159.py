# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0010_auto_20170426_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idc',
            name='user',
        ),
        migrations.AddField(
            model_name='idc',
            name='user',
            field=models.ForeignKey(default=2, to='dashborad.Userprofile'),
            preserve_default=False,
        ),
    ]
