# Generated by Django 4.2.1 on 2024-01-12 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0007_gamebox_challenge_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamebox',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
