# Generated by Django 2.1.1 on 2018-09-26 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomLogger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('logger', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('level', models.PositiveIntegerField(blank=True, choices=[(0, 'NOTSET'), (50, 'CRITICAL'), (40, 'ERROR'), (30, 'WARNING'), (20, 'INFO'), (10, 'DEBUG')], db_index=True, default=40)),
                ('message', models.TextField(blank=True, null=True)),
                ('formatted', models.TextField(blank=True, null=True)),
                ('server_name', models.CharField(db_index=True, max_length=128)),
                ('pathname', models.TextField(blank=True, null=True)),
                ('lineno', models.IntegerField(blank=True, null=True)),
                ('filename', models.TextField(blank=True, null=True)),
                ('module', models.TextField(blank=True, null=True)),
                ('func_name', models.TextField(blank=True, null=True)),
                ('process', models.TextField(blank=True, null=True)),
                ('traceback', models.TextField(blank=True, null=True)),
                ('exc_type', models.TextField(blank=True, null=True)),
                ('extra', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
