# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0015_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf\xe5\x90\x8d\xe7\xa7\xb0')),
                ('module_letter', models.CharField(max_length=10, verbose_name=b'\xe5\xad\x97\xe6\xaf\x8d\xe7\xae\x80\xe7\xa7\xb0')),
                ('op_interface', models.CharField(max_length=255, verbose_name=b'\xe8\xbf\x90\xe7\xbb\xb4\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba: username1,username2')),
                ('dev_interface', models.CharField(max_length=255, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba: username1,username2')),
                ('p_product', models.ForeignKey(verbose_name=b'\xe4\xb8\x8a\xe7\xba\xa7\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf', to='dashborad.Product', null=True)),
            ],
            options={
                'db_table': 'product',
                'permissions': (('view_product', '\u8bbf\u95ee\u4e1a\u52a1\u7ebf'),),
            },
        ),
    ]
