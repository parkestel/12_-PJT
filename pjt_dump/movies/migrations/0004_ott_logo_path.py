# Generated by Django 4.2.11 on 2024-11-13 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_ott'),
    ]

    operations = [
        migrations.AddField(
            model_name='ott',
            name='logo_path',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
