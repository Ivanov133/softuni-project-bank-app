# Generated by Django 4.0.3 on 2022-04-13 12:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks_app', '0003_remove_usertask_task_type1_alter_usertask_task_type'),
        ('customer_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='IndividualCustomer',
        ),
    ]
