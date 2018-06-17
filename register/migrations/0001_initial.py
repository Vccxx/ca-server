# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-22 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SerialNumber', models.CharField(max_length=4096)),
                ('Subject', models.CharField(max_length=128)),
                ('PublicKey', models.CharField(max_length=2048)),
                ('PublicKeyAlgorithm', models.CharField(max_length=128)),
                ('Fingerprint', models.CharField(max_length=2048)),
                ('FingerprintAlgorithm', models.CharField(max_length=128)),
                ('ValidTo', models.DateField()),
                ('originSignature', models.CharField(max_length=4096)),
                ('SignatureAlgorithm', models.CharField(max_length=128)),
            ],
        ),
    ]