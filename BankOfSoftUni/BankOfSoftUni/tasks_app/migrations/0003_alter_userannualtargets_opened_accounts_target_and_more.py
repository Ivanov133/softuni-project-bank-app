# Generated by Django 4.0.3 on 2022-04-27 18:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0002_remove_userannualtargets_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userannualtargets',
            name='opened_accounts_target',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='userannualtargets',
            name='opened_loans_count_target',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='userannualtargets',
            name='registered_clients_target',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='userannualtargets',
            name='total_loans_size_target',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
