# Generated by Django 4.0.5 on 2022-10-25 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_playerorder_game_joined_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction_id', models.IntegerField()),
                ('token', models.IntegerField(null=True)),
                ('dice_result', models.IntegerField(null=True)),
                ('action', models.TextField()),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.game')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.users')),
            ],
        ),
    ]