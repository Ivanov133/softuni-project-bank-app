import datetime
from django import forms

from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.helpers.common import get_next_month_date


class CreateLoanForm(forms.ModelForm):
    def __init__(self, accounts, customer, user, interest_rate, monthly_payment,
                 principal, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = accounts
        self.customer = customer
        self.user = user
        self.interest_rate = interest_rate
        self.monthly_payment = monthly_payment
        self.next_monthly_payment_due_date = get_next_month_date()
        self.principal = principal
        self.period = period
        self.initial['principal'] = principal
        self.initial['interest_rate'] = interest_rate
        self.initial['duration_in_years'] = period
        self.initial['next_monthly_payment_due_date'] = self.next_monthly_payment_due_date
        self.initial['monthly_payment_value'] = monthly_payment
        self.initial['customer_debtor'] = customer
        self.initial['assigned_user'] = user

        # disable all fields and handle account choices
        for name, field in self.fields.items():
            if not name == 'account_credit':
                field.widget.attrs['disabled'] = 'disabled'
            else:
                field.choices = ((x, x) for x in [acc.account_number for acc in accounts])

    class Meta:
        model = BankLoan
        fields = (
            'principal',
            'interest_rate',
            'duration_in_years',
            'next_monthly_payment_due_date',
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
