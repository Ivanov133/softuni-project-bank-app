# Generated by Django 4.0.3 on 2022-04-19 19:32

import BankOfSoftUni.helpers.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('BGN', 'BGN'), ('USD', 'USD'), ('CHF', 'CHF'), ('GBP', 'GBP'), ('JPY', 'JPY'), ('EUR', 'EUR')], max_length=40)),
                ('open_date', models.DateTimeField(auto_now_add=True)),
                ('available_balance', models.FloatField(default=0)),
                ('debit_card', models.CharField(choices=[('VISA', 'VISA'), ('MASTERCARD', 'MASTERCARD')], max_length=20)),
                ('assigned_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IndividualCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40, validators=[BankOfSoftUni.helpers.validators.validate_only_letters])),
                ('sir_name', models.CharField(blank=True, max_length=40, null=True, validators=[BankOfSoftUni.helpers.validators.validate_only_letters])),
                ('last_name', models.CharField(max_length=40, validators=[BankOfSoftUni.helpers.validators.validate_only_letters])),
                ('ucn', models.BigIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('document_number', models.CharField(max_length=25, unique=True)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('annual_income', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('occupation', models.CharField(blank=True, default='unemployed', max_length=40, null=True, validators=[BankOfSoftUni.helpers.validators.validate_only_letters])),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('date_of_birth', models.DateField()),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('id_card', models.ImageField(upload_to='customer_images')),
                ('assigned_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankLoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('BGN', 'BGN')], max_length=40)),
                ('principal', models.FloatField(validators=[django.core.validators.MaxValueValidator(500000), django.core.validators.MinValueValidator(1000)])),
                ('interest_rate', models.FloatField()),
                ('duration_in_months', models.IntegerField(validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(12)])),
                ('duration_remainder_months', models.IntegerField(default=models.IntegerField(validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(12)]))),
                ('principal_remainder', models.FloatField(default=models.FloatField(validators=[django.core.validators.MaxValueValidator(500000), django.core.validators.MinValueValidator(1000)]))),
                ('next_monthly_payment_due_date', models.DateTimeField()),
                ('monthly_payment_value', models.FloatField()),
                ('is_paid_monthly', models.BooleanField(default=False)),
                ('open_date', models.DateTimeField(auto_now_add=True)),
                ('account_credit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer_manager.account')),
                ('assigned_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('customer_debtor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer_manager.individualcustomer')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_accounts', to='customer_manager.individualcustomer'),
        ),
    ]
