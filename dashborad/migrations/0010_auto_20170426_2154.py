# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0009_auto_20170426_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idc',
            name='user_email',
        ),
        migrations.RemoveField(
            model_name='idc',
            name='user_phone',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default=2, max_length=32),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='idc',
            name='user',
        ),
        migrations.AddField(
            model_name='idc',
            name='user',
            field=models.ManyToManyField(to='dashborad.Userprofile'),
        ),
    ]
