# Generated by Django 4.0.5 on 2023-01-06 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_acceptancelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerorder',
            name='colour',
            field=models.TextField(default='black'),
            preserve_default=False,
        ),
    ]
