# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0004_auto_20170420_0248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'permissions': (('view_userlist', 'can view userlist'), ('view_grouplist', 'can view grouplist'), ('view_groupuser', 'can view group user'), ('add_groupuser', 'can add group user'), ('del_groupuser', 'can add group user'))},
        ),
    ]
