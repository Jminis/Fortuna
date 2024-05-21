# Generated by Django 5.0.1 on 2024-05-21 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('challenge_id', models.PositiveIntegerField(blank=True, null=True)),
                ('challenge_name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('ip', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'challenges',
            },
        ),
        migrations.CreateModel(
            name='GameBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('team_id', models.PositiveIntegerField(blank=True)),
                ('challenge_id', models.PositiveIntegerField(blank=True)),
                ('ip', models.CharField(blank=True, max_length=255, null=True)),
                ('port', models.PositiveIntegerField(blank=True, null=True)),
                ('ssh_port', models.PositiveIntegerField(blank=True, null=True)),
                ('ssh_user', models.CharField(blank=True, max_length=255, null=True)),
                ('ssh_password', models.CharField(blank=True, max_length=255, null=True)),
                ('visible', models.BooleanField(blank=True, default=True)),
                ('point_down', models.IntegerField()),
                ('point_attack', models.IntegerField()),
                ('is_down', models.BooleanField(blank=True, default=False)),
                ('is_attacked', models.BooleanField(blank=True, default=False)),
            ],
            options={
                'db_table': 'game_boxes',
            },
        ),
    ]
