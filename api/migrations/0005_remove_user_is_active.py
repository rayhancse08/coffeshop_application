# Generated by Django 2.0.3 on 2018-11-30 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
    ]
