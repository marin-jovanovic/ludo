# Generated by Django 4.0.5 on 2023-01-10 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_playerorder_colour'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptancelog',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
    ]