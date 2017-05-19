# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0012_auto_20170427_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier', models.IntegerField(null=True)),
                ('manufacturers', models.CharField(max_length=50, null=True)),
                ('manufacture_date', models.DateField(null=True)),
                ('server_type', models.CharField(max_length=20, null=True)),
                ('sn', models.CharField(max_length=60, null=True, db_index=True)),
                ('os', models.CharField(max_length=50, null=True)),
                ('hostname', models.CharField(max_length=50, null=True, db_index=True)),
                ('inner_ip', models.CharField(max_length=32, unique=True, null=True)),
                ('mac_address', models.CharField(max_length=50, null=True)),
                ('ip_info', models.CharField(max_length=255, null=True)),
                ('server_cpu', models.CharField(max_length=250, null=True)),
                ('server_disk', models.CharField(max_length=100, null=True)),
                ('server_mem', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True, db_index=True)),
                ('remark', models.TextField(null=True)),
                ('check_update_time', models.DateTimeField(null=True)),
                ('vm_status', models.IntegerField(null=True, db_index=True)),
                ('uuid', models.CharField(max_length=100, null=True, db_index=True)),
                ('idc', models.ForeignKey(to='dashborad.Idc', null=True)),
            ],
            options={
                'db_table': 'server',
                'permissions': (('view_server', '\u8bbf\u95ee\u670d\u52a1\u5668\u4fe1\u606f'),),
            },
        ),
    ]
