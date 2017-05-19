# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0006_auto_20170421_0341'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'permissions': (('view_userlist', 'can view userlist'), ('view_grouplist', 'can view grouplist'), ('view_groupuser', 'can view group user'), ('add_groupuser', 'can add group user'), ('del_groupuser', 'can del group user'), ('view_usergroup', 'can view user group'))},
        ),
    ]
