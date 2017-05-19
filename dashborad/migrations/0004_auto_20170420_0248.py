# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0003_auto_20170412_0811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'permissions': (('view_userlist', 'can view userlist'), ('view_grouplist', 'can view grouplist'))},
        ),
    ]
