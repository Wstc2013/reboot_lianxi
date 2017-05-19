# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0008_auto_20170421_0736'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=10, verbose_name=b'idc \xe5\xad\x97\xe6\xaf\x8d\xe7\xae\x80\xe7\xa7\xb0')),
                ('idc_name', models.CharField(max_length=100, verbose_name=b'idc \xe4\xb8\xad\xe6\x96\x87\xe5\x90\x8d')),
                ('address', models.CharField(max_length=255, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf\xe7\x9a\x84\xe5\x85\xb7\xe4\xbd\x93\xe5\x9c\xb0\xe5\x9d\x80')),
                ('user', models.CharField(max_length=32, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba')),
                ('user_phone', models.IntegerField(max_length=20, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba\xe7\x94\xb5\xe8\xaf\x9d')),
                ('user_email', models.EmailField(max_length=32, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba\xe9\x82\xae\xe7\xae\xb1')),
            ],
            options={
                'db_table': 'idc',
                'permissions': (('view_idc', 'can view idc'),),
            },
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'permissions': (('view_userlist', 'can view userlist'), ('view_grouplist', 'can view grouplist'), ('view_groupuser', 'can view group user'), ('add_groupuser', 'can add group user'), ('del_groupuser', 'can del group user'), ('view_usergroup', 'can view user group'), ('add_usergroup', 'can add user group'), ('change_groupermission', 'can change group permission'))},
        ),
    ]
