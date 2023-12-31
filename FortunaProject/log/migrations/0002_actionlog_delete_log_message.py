# Generated by Django 4.2.7 on 2023-11-23 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('team_id', models.PositiveIntegerField(blank=True, null=True)),
                ('challenge_id', models.PositiveIntegerField(blank=True, null=True)),
                ('game_box_id', models.PositiveIntegerField(blank=True, null=True)),
                ('attacker_team_id', models.PositiveIntegerField(blank=True, null=True)),
                ('round', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'action_log',
            },
        ),
        migrations.DeleteModel(
            name='log_Message',
        ),
    ]
