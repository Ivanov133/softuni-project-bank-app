# Generated by Django 4.0.3 on 2022-04-02 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_alter_bankuser_is_staff_alter_bankuser_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]
