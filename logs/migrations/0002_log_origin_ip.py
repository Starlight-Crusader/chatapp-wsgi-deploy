# Generated by Django 4.2.6 on 2024-01-22 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='origin_ip',
            field=models.CharField(null=True),
        ),
    ]
