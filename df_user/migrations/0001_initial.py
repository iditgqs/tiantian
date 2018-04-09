# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddrInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ushou', models.CharField(max_length=20)),
                ('uaddress', models.CharField(max_length=100)),
                ('uyoubian', models.CharField(max_length=6)),
                ('uphone', models.CharField(default=b'', max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(unique=True, max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='addrinfo',
            name='user',
            field=models.ForeignKey(to='df_user.UserInfo'),
        ),
    ]
