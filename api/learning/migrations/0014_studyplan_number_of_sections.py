# Generated by Django 3.2.19 on 2023-07-20 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0013_alter_studyplan_total_spent'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyplan',
            name='number_of_sections',
            field=models.IntegerField(default=5),
        ),
    ]
