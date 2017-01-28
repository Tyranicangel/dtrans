# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_fins_horizontal_vertical'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('customer', models.CharField(max_length=100)),
                ('referenceno', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=20)),
                ('voltagelv', models.CharField(max_length=20)),
                ('voltagehv', models.CharField(max_length=20)),
                ('connection', models.CharField(max_length=20)),
                ('noloadloss', models.DecimalField(max_digits=20, decimal_places=3)),
                ('loadloss', models.DecimalField(max_digits=20, decimal_places=3)),
                ('impedance', models.DecimalField(max_digits=20, decimal_places=3)),
                ('costing', models.DecimalField(max_digits=20, decimal_places=3)),
                ('designdata', models.TextField()),
                ('designuser', models.ForeignKey(related_name=b'design_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
