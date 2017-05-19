# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0013_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='check_update_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
