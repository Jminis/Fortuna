# Generated by Django 3.2.12 on 2024-03-26 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_team_secret_key_alter_team_team_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]