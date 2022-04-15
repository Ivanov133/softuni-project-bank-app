from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from BankOfSoftUni.auth_app.models import Profile, BankUser
from BankOfSoftUni.helpers.common import calc_foreign_currency_to_BGN, get_loan_end_date
from BankOfSoftUni.helpers.validators import validate_only_letters


class IndividualCustomer(models.Model):
    MAX_FIRST_NAME_LEN = 40
    MAX_SIR_NAME_LEN = 40
    MAX_LAST_NAME_LEN = 40

    DOCUMENT_NUMBER_MAX_LEN = 25
    IMAGE_UPLOAD_DIR = 'customer_images'

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LEN,
        validators=(
            validate_only_letters,
        )
    )

    # Foreign clients may not have sirname
    sir_name = models.CharField(
        max_length=MAX_SIR_NAME_LEN,
        blank=True,
        null=True,
        validators=(
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LEN,
        validators=(
            validate_only_letters,
        )
    )

    ucn = models.BigIntegerField(
        unique=True,
        validators=(
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999),
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
        validators=(
            validate_only_letters,
        )
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

    id_card = models.ImageField(
        upload_to=IMAGE_UPLOAD_DIR,
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.sir_name} {self.last_name}'

    @property
    def customer_number(self):
        return f'CUS{1000 + self.id}'


class Account(models.Model):
    ALLOWED_CURRENCIES = (
        'BGN',
        'USD',
        'CHF',
        'GBP',
        'JPY',
        'EUR',
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
        IndividualCustomer,
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

    def __str__(self):
        return str(self.id)

    # TO DO - create card and IBAN generators, depending on user branch etc.
    @property
    def account_number(self):
        return f'BG13SOFT{8550120070001 + self.id}'

    @property
    def debit_card_number(self):
        return f'{4550 + self.id} XXXX XXXX {1250 + self.id}'

    @property
    def local_currency(self):
        return calc_foreign_currency_to_BGN(self.available_balance, self.currency)


class BankLoan(models.Model):
    # TO DO ADD FIXTURES
    ALLOWED_CURRENCIES = (
        'BGN',
    )

    MAX_LOAN_PRINCIPAL = 500000
    MIN_LOAN_PRINCIPAL = 1000
    MAX_LOAN_DURATION_IN_YEARS = 30
    MIN_LOAN_DURATION_IN_YEARS = 1

    currency = models.CharField(
        choices=[(x, x) for x in ALLOWED_CURRENCIES],
        max_length=40,
    )
    # initial value of the loan
    principal = models.FloatField(
        validators=(
            MaxValueValidator(MAX_LOAN_PRINCIPAL),
            MinValueValidator(MIN_LOAN_PRINCIPAL),
        )
    )

    interest_rate = models.FloatField()

    duration_in_years = models.IntegerField(
        validators=(
            MaxValueValidator(MAX_LOAN_DURATION_IN_YEARS),
            MinValueValidator(MIN_LOAN_DURATION_IN_YEARS),
        )
    )

    principal_remainder = models.FloatField(
        default=principal,
    )

    next_monthly_payment_due_date = models.DateTimeField()

    monthly_payment_value = models.FloatField()

    is_paid_monthly = models.BooleanField(
        default=False,
    )

    customer_debtor = models.ForeignKey(
        IndividualCustomer,
        on_delete=models.DO_NOTHING,
    )

    assigned_user = models.ForeignKey(
        BankUser,
        on_delete=models.DO_NOTHING,
    )

    account_credit = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
    )

    open_date = models.DateTimeField(
        auto_now_add=True,
    )


    @property
    def loan_number(self):
        return f'LN{self.customer_debtor.customer_number}{self.currency}'

    @property
    def end_date(self):
        return get_loan_end_date(self.open_date, self.duration_in_years)
