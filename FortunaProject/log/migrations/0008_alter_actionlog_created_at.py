# Generated by Django 4.2.7 on 2023-11-25 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0007_alter_actionlog_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionlog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]