# Generated by Django 3.2.19 on 2023-07-06 21:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0014_alter_token_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 21, 8, 11, 299078, tzinfo=utc)),
        ),
    ]
