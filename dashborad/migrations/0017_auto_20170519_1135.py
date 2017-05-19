# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashborad', '0016_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='server_business',
            field=models.ForeignKey(related_name='server_business', to='dashborad.Product', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='server_product',
            field=models.ForeignKey(related_name='server_product', to='dashborad.Product', null=True),
        ),
    ]
