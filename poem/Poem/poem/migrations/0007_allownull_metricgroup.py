# Generated by Django 2.0.7 on 2018-11-06 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0006_set_passive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='poem.GroupOfMetrics'),
        ),
    ]