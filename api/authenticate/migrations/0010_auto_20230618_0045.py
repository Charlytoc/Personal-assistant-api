# Generated by Django 3.2.19 on 2023-06-18 00:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0009_alter_token_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providercredentials',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2023, 8, 17)),
        ),
        migrations.AlterField(
            model_name='token',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 18, 0, 45, 53, 735897, tzinfo=utc)),
        ),
    ]
