# Generated by Django 3.2.19 on 2023-07-06 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='communities',
            field=models.ManyToManyField(null=True, to='learning.Community'),
        ),
    ]
