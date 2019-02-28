# Generated by Django 2.0.13 on 2019-02-24 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0013_aggregation_groupname'),
    ]

    operations = [
        migrations.AddField(
            model_name='custuser',
            name='groupsofaggregations',
            field=models.ManyToManyField(blank=True, help_text='The groups of aggregations that this user belongs to', related_name='user_set', related_query_name='user', to='poem.GroupOfAggregations', verbose_name='groups of aggregations'),
        ),
    ]
