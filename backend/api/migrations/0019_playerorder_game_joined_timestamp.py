# Generated by Django 4.0.5 on 2022-10-25 09:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_playerorder_index_left_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerorder',
            name='game_joined_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
