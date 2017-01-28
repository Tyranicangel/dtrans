# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_revisions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='designs',
            name='costing',
        ),
        migrations.RemoveField(
            model_name='designs',
            name='designdata',
        ),
        migrations.RemoveField(
            model_name='designs',
            name='designuser',
        ),
        migrations.RemoveField(
            model_name='designs',
            name='impedance',
        ),
        migrations.RemoveField(
            model_name='designs',
            name='loadloss',
        ),
        migrations.RemoveField(
            model_name='designs',
            name='noloadloss',
        ),
        migrations.AddField(
            model_name='revisions',
            name='remarks',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='revisions',
            name='revisionno',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
