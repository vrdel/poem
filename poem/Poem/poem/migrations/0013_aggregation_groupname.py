# Generated by Django 2.0.13 on 2019-02-24 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0012_aggregation_groupofaggregations'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggregation',
            name='groupname',
            field=models.CharField(default='', max_length=128),
        ),
    ]
