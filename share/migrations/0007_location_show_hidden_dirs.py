# Generated by Django 2.0.1 on 2018-01-31 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0006_auto_20180131_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='show_hidden_dirs',
            field=models.BooleanField(default=False),
        ),
    ]