# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-04 13:37
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GSCapabilitySet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'View Only', max_length=100, unique=True)),
                ('load_profile', models.BooleanField(default=False)),
                ('outage_mgmt', models.BooleanField(default=False)),
                ('editing', models.BooleanField(default=False)),
                ('power_flow', models.BooleanField(default=False)),
                ('model_editing', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GSGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capabilities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.GSCapabilitySet')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GSInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'EPE', max_length=100, unique=True)),
                ('gis_server', models.CharField(default=b'', max_length=100)),
                ('db_server', models.CharField(default=b'', max_length=100)),
                ('db_instance', models.CharField(default=b'', max_length=100)),
                ('map_instance', models.CharField(default=b'', max_length=100)),
                ('sde_instance', models.CharField(default=b'', max_length=100)),
                ('sde_pfx', models.CharField(default=b'', max_length=100)),
                ('grid_instance', models.CharField(default=b'', max_length=100)),
                ('capabilities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.GSCapabilitySet')),
            ],
        ),
        migrations.CreateModel(
            name='GSOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('instances', models.ManyToManyField(to='polls.GSInstance')),
            ],
        ),
        migrations.CreateModel(
            name='GSUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.GSInstance')),
                ('group', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field=b'org', chained_model_field=b'org', on_delete=django.db.models.deletion.CASCADE, to='polls.GSGroup')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.GSOrg')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='gsgroup',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.GSOrg'),
        ),
    ]