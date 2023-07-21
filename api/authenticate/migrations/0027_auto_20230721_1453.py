# Generated by Django 3.2.19 on 2023-07-21 14:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0026_auto_20230720_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providercredentials',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2023, 9, 19)),
        ),
        migrations.AlterField(
            model_name='token',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 20, 14, 53, 24, 221791, tzinfo=utc)),
        ),
    ]