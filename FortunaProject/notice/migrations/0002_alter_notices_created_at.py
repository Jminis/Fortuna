# Generated by Django 4.2.1 on 2024-01-16 02:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notices',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
