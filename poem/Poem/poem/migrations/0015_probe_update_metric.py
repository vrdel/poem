# Generated by Django 2.0.9 on 2019-02-20 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0014_custuser_groupsofaggregations'),
    ]

    operations = [
        migrations.AddField(
            model_name='probe',
            name='update_metric',
            field=models.NullBooleanField(default=True),
        ),
    ]
