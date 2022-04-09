from django.core.validators import MinValueValidator
from django.db import models

from BankOfSoftUni.auth_app.models import Profile, BankUser


class Customer(models.Model):
    MAX_FIRST_NAME_LEN = 40
    MAX_SIR_NAME_LEN = 40
    MAX_LAST_NAME_LEN = 40

    DOCUMENT_NUMBER_MAX_LEN = 25

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LEN,
    )

    # Foreign clients may not have sirname
    sir_name = models.CharField(
        max_length=MAX_SIR_NAME_LEN,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LEN,
    )

    ucn = models.BigIntegerField(
        unique=True,
        validators=(
            MinValueValidator(0),
        ),
    )

    document_number = models.CharField(
        max_length=25,
        unique=True,
    )

    age = models.IntegerField(
        validators=(
            MinValueValidator(0),
        ),
    )

    annual_income = models.IntegerField(
        validators=(
            MinValueValidator(0),
        ),
        default=0,
        blank=True,
        null=True,
    )

    occupation = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        default='unemployed',
    )

    gender = models.CharField(
        max_length=6,
        choices=[(x, x) for x in ('Male', 'Female')]
    )

    date_of_birth = models.DateField()

    assigned_user = models.ForeignKey(
        BankUser,
        on_delete=models.DO_NOTHING,
    )

    registration_date = models.DateTimeField(
        auto_now_add=True,
    )

    id_card = models.URLField()

    @property
    def full_name(self):
        return f'{self.first_name} {self.sir_name} {self.last_name}'

    @property
    def customer_number(self):
        return f'SOFTU{100000 + self.id}'


class Account(models.Model):
    ALLOWED_CURRENCIES = (
        'BGN',
        'USD',
        'CHF',
        'GBP',
        'JPY',
    )

    BANK_CARD_MANUFACTURER = (
        'VISA',
        'MASTERCARD',
    )
    currency = models.CharField(
        choices=[(x, x) for x in ALLOWED_CURRENCIES],
        max_length=40,
    )
    open_date = models.DateTimeField(
        auto_now_add=True,
    )

    available_balance = models.FloatField(
        default=0,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
        related_name='customer_accounts',
    )

    debit_card = models.CharField(
        choices=[(x, x) for x in BANK_CARD_MANUFACTURER],
        max_length=20,
    )
    assigned_user = models.ForeignKey(
        BankUser,
        on_delete=models.DO_NOTHING,
    )

    # TO DO - create card and IBAN generators, depending on user branch etc.
    @property
    def account_number(self):
        return f'BG13SOFT{8550120070001 + self.id}'

    @property
    def debit_card_number(self):
        return f'{4550 + self.id} XXXX XXXX {1250 + self.id}'
