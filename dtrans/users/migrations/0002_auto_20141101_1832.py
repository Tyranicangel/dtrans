# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='designation',
            field=models.CharField(default=b'Admin', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default=b'1', max_length=20),
            preserve_default=True,
        ),
    ]
