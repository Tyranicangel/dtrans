# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('core', models.CharField(max_length=20)),
                ('flux', models.CharField(max_length=20)),
                ('frequency', models.CharField(max_length=20)),
                ('factor', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Radiators',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('pannel', models.CharField(max_length=20)),
                ('length', models.CharField(max_length=20)),
                ('sarea_sec', models.CharField(max_length=20)),
                ('deg35', models.CharField(max_length=20)),
                ('deg40', models.CharField(max_length=20)),
                ('deg45', models.CharField(max_length=20)),
                ('deg50', models.CharField(max_length=20)),
                ('deg55', models.CharField(max_length=20)),
                ('deg60', models.CharField(max_length=20)),
                ('wt_sec', models.CharField(max_length=20)),
                ('oil_sec', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
