import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.helpers.common import get_next_month_date, update_target_list_customer, \
    clear_request_session_loan_params, update_target_list_loans, \
    calc_local_currency_to_foreign


class CreateLoanForm(forms.ModelForm):
    def __init__(self, user, principal, interest_rate, monthly_payment, customer, accounts, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.accounts = accounts
        self.principal = principal
        self.period = period
        self.interest_rate = interest_rate
        self.monthly_payment = monthly_payment
        self.customer = customer
        self.initial['principal'] = self.principal
        self.initial['interest_rate'] = self.interest_rate
        self.initial['duration_in_months'] = self.period
        self.initial['monthly_payment_value'] = self.monthly_payment
        self.fields['account_credit'].choices = [(acc, acc.account_number) for acc in self.accounts]
        for name, field in self.fields.items():
            if not name == 'account_credit':
                field.widget.attrs['readonly'] = True

    def save(self, commit=True):
        loan = BankLoan(
            principal=self.cleaned_data['principal'],
            interest_rate=self.cleaned_data['interest_rate'],
            duration_in_months=self.cleaned_data['duration_in_months'],
            duration_remainder_months=self.cleaned_data['duration_in_months'],
            monthly_payment_value=self.cleaned_data['monthly_payment_value'],
            account_credit=self.cleaned_data['account_credit'],
            assigned_user=self.user,
            customer_debtor=self.customer,
            currency=self.cleaned_data['currency'],
            principal_remainder=self.cleaned_data['principal'],
            next_monthly_payment_due_date=get_next_month_date(),
            account_credit_id=self.cleaned_data['account_credit'].id,
        )

        if commit:
            # Add balance to account
            # Add loan to target list
            # save loan
            account = Account.objects.get(pk=self.cleaned_data['account_credit'].id)
            account.available_balance += calc_local_currency_to_foreign(float(self.cleaned_data['principal']),
                                                                        account.currency)
            account.save()

            update_target_list_loans(self.user.id, self.cleaned_data['principal'])

            loan.save()

        return loan

    class Meta:
        model = BankLoan
        fields = (
            'currency',
            'principal',
            'interest_rate',
            'duration_in_months',
            'monthly_payment_value',
            'account_credit',
        )


class CreateCustomerForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.assigned_user = self.user

        # Update target list in db - add one customer
        update_target_list_customer(self.user.id)

        if commit:
            customer.save()

        return customer

    class Meta:
        model = IndividualCustomer
        this_year = datetime.date.today().year
        year_range = [x for x in range(this_year - 100, this_year + 1)]
        fields = (
            'first_name',
            'sir_name',
            'last_name',
            'ucn',
            'document_number',
            'age',
            'occupation',
            'annual_income',
            'id_card',
            'date_of_birth',
            'gender',

        )

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'sir_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter sir name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
            'ucn': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter Unique Citizenship Number',
                }
            ),
            'document_number': forms.TextInput(
                attrs={
                    'placeholder': 'Enter ID/Passport number',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'placeholder': 'Client age',
                }
            ),
            'annual_income': forms.NumberInput(
                attrs={
                }
            ),
            'date_of_birth': forms.SelectDateWidget(years=year_range),

        }


class AccountOpenForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'currency',
            'debit_card',
        )


class LoanEditForm(forms.ModelForm):
    # MAX_LOAN_ =
    # MIN_CASH_DEPOSIT_VALUE = 1

    def __init__(self, accounts, loans, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = accounts
        self.loans = loans
        self.fields['accounts'] = forms.ChoiceField(
            choices=[(acc, acc.account_number) for acc in self.accounts],
            label='Choose debit account'
        )
        self.fields['loans'] = forms.ChoiceField(
            choices=[(loan, loan.loan_number) for loan in self.loans],
            label='Choose loan'
        )
        self.fields['loan_payment'] = forms.IntegerField(
            label='Choose loan payment size',
            validators=[
                    MinValueValidator(MIN_CASH_DEPOSIT_VALUE, f'Minimum deposit is {MIN_CASH_DEPOSIT_VALUE} currency unit'),
                    MaxValueValidator(MAX_CASH_DEPOSIT_VALUE, f'Maximum deposit is {MAX_CASH_DEPOSIT_VALUE} currency unit')
                ]
        )

    def clean(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password_confirm'):
            self.add_error('password_confirm', "passwords do not match !")
        return cd

    def save(self, commit=True):
        account = self.cleaned_data['accounts']
        loan = self.cleaned_data['loans']
        raise forms.ValidationError('test')

    class Meta:
        model = BankLoan
        fields = ()
        labels = {
            'accounts': 'Repay principal by'
        }


class AccountEditForm(forms.ModelForm):
    MAX_CASH_DEPOSIT_VALUE = 1000000
    MIN_CASH_DEPOSIT_VALUE = 1
    cash_deposit = forms.DecimalField(
        validators=[
            MinValueValidator(MIN_CASH_DEPOSIT_VALUE, f'Minimum deposit is {MIN_CASH_DEPOSIT_VALUE} currency unit'),
            MaxValueValidator(MAX_CASH_DEPOSIT_VALUE, f'Maximum deposit is {MAX_CASH_DEPOSIT_VALUE} currency unit')
        ],
    )

    def __init__(self, accounts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = accounts
        self.fields['accounts'] = forms.ChoiceField(
            choices=[(acc, acc.account_number) for acc in self.accounts]
        )

    def save(self, commit=True):
        account = Account.objects.filter(pk=self.cleaned_data['accounts']).get()
        account.available_balance += float(self.cleaned_data['cash_deposit'])

        if commit:
            account.save()

    class Meta:
        model = Account
        fields = ()


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = IndividualCustomer
        fields = (
            'first_name',
            'sir_name',
            'last_name',
            'ucn',
            'document_number',
            'age',
            'occupation',
            'annual_income',
            'id_card',
            'date_of_birth',
            'gender',
        )
