# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0017_auto_20170519_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZabbixHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zabbix_hostid', models.IntegerField(null=True, verbose_name=b'zabbix_hostid', db_index=True)),
                ('zabbix_hostname', models.CharField(max_length=32, null=True, verbose_name=b'zabbix_hostname', db_index=True)),
                ('zabbix_ip', models.CharField(max_length=32, null=True, verbose_name=b'zabbix_ip', db_index=True)),
                ('updatetime', models.DateField(auto_now=True)),
                ('server', models.OneToOneField(null=True, to='dashborad.Server')),
            ],
            options={
                'db_table': 'resource_zabbix_cache',
            },
        ),
    ]
