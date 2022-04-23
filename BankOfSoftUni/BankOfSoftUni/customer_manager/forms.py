import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.helpers.common import get_next_month_date, update_target_list_customer, \
    clear_request_session_loan_params, update_target_list_loans, \
    calc_local_currency_to_foreign, calculate_new_loan_payment
from BankOfSoftUni.helpers.parametrizations import ALLOWED_CURRENCIES


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
        self.fields['account_credit'].choices = [(acc.id, acc.account_number) for acc in self.accounts]
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


class LoanEditForm(forms.ModelForm):
    MIN_LOAN_PREMATURE_PAYMENT = 1
    LOAN_PREMATURE_PAYMENT_TYPES = [
        ('Reduce monthly payment', 'Reduce monthly payment'),
        ('Reduce loan end date', 'Reduce loan end date'),
    ]

    loan_change_type = forms.ChoiceField(
        choices=LOAN_PREMATURE_PAYMENT_TYPES,
    )

    def __init__(self, accounts, loan, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = accounts
        self.loan = loan
        self.fields['accounts'] = forms.ChoiceField(
            choices=[(acc.id, acc.account_number) for acc in self.accounts],
            label='Choose debit account or make deposit'
        )
        self.fields['accounts'].choices.append(('Cash deposit', 'Cash deposit'))
        self.fields['loan_payment'] = forms.DecimalField(
            label='Choose loan payment size',
            validators=[
                MinValueValidator(self.MIN_LOAN_PREMATURE_PAYMENT,
                                  f'Minimum payment is {self.MIN_LOAN_PREMATURE_PAYMENT} currency unit'),
            ]
        )

    def clean(self):
        cleaned_data = super().clean()
        loan_payment = float(self.cleaned_data['loan_payment'])
        if not self.cleaned_data['accounts'] == 'Cash deposit':
            account = Account.objects.get(pk=self.cleaned_data['accounts'])
            if loan_payment > account.local_currency:
                self.add_error('loan_payment', 'Account balance is not enough to make payment!')

        if loan_payment > self.loan.principal_remainder:
            self.add_error('loan_payment', 'Loan payment cannot exceed remaining principal!')

        return self.cleaned_data

    def save(self, commit=True):
        loan = self.loan
        loan_payment = float(self.cleaned_data['loan_payment'])
        new_monthly_payment = None
        # new_period = None
        if self.cleaned_data['loan_change_type'] == 'Reduce monthly payment':
            new_monthly_payment = calculate_new_loan_payment(
                loan.interest_rate / 100,
                loan.principal_remainder - loan_payment,
                loan.duration_remainder_months
            )
        # elif self.cleaned_data['loan_change_type'] == 'Reduce loan end date':
        #     new_period = calculate_new_loan_period(
        #         loan.interest_rate / 100,
        #         loan.principal_remainder,
        #         loan.monthly_payment_value
        #     )

        # If an account is chosen - it's balance must be reduced
        # When the loan principal is reduced, new calculations must be made,
        # depending on what is chosen in the form - we either reduce the monthly payment
        # and keep the end period, or we keep the payment and reduce the period
        if commit:
            if not self.cleaned_data['accounts'] == 'Cash deposit':
                account = Account.objects.get(pk=self.cleaned_data['accounts'])
                account.available_balance -= loan_payment / ALLOWED_CURRENCIES[f'{account.currency}']
                account.save()
            if new_monthly_payment:
                loan.monthly_payment_value = float(new_monthly_payment)
            else:
                loan.duration_remainder_months = (loan.principal_remainder - loan_payment) / loan.monthly_payment_value

            loan.principal_remainder -= loan_payment
            loan.save()

    class Meta:
        model = BankLoan
        fields = ()
        labels = {
            'accounts': 'Repay principal by'
        }


class CustomerDeleteForm(forms.ModelForm):
    pass


class AccountDeleteForm(forms.ModelForm):
    def __init__(self, debit_account, all_accounts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debit_account = debit_account
        self.all_accounts = all_accounts
        self.fields['all_accounts'] = forms.ChoiceField(
            choices=[(acc.id, acc.account_number) for acc in self.all_accounts if not acc == self.debit_account],
            label=f'Transfer {self.debit_account.account_number} balance to another account or make cash withdrawal',
            required=False,
        )
        self.fields['all_accounts'].choices.append(('Cash withdrawal', 'Cash withdrawal'))

    class Meta:
        model = Account
        fields = ()


class AccountEditForm(forms.ModelForm):
    MAX_CASH_DEPOSIT_VALUE = 1000000
    MIN_CASH_DEPOSIT_VALUE = 1
    cash_deposit = forms.DecimalField(
        label=f'Cash deposit in same currency as account',
        validators=[
            MinValueValidator(MIN_CASH_DEPOSIT_VALUE, f'Minimum deposit is {MIN_CASH_DEPOSIT_VALUE} currency unit'),
            MaxValueValidator(MAX_CASH_DEPOSIT_VALUE, f'Maximum deposit is {MAX_CASH_DEPOSIT_VALUE} currency unit')
        ],
    )

    def __init__(self, account, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account = account
        self.fields['account'] = forms.CharField()
        self.fields['account'].widget.attrs['readonly'] = True
        self.fields['available_balance'].label = f'Current balance in {self.account.currency}   '
        self.fields['available_balance'].widget.attrs['readonly'] = True
        self.initial['account'] = self.account.account_number

    def save(self, commit=True):
        account = self.account
        account.available_balance += float(self.cleaned_data['cash_deposit'])
        if float(self.cleaned_data['cash_deposit']) < 0:
            raise ValidationError('Invalid deposit input')

        if commit:
            account.save()

    class Meta:
        model = Account
        fields = ('available_balance',)


class LoanDeleteForm(forms.ModelForm):
    def __init__(self, loan, accounts, *args, **kwargs):
        super(LoanDeleteForm, self).__init__(*args, **kwargs)
        self.loan = loan
        self.accounts = accounts
        self.fields['accounts'] = forms.ChoiceField(
            choices=[(acc.id, acc.account_number) for acc in self.accounts],
            label='Choose debit account or make deposit'
        )
        self.fields['accounts'].choices.append(('Cash deposit', 'Cash deposit'))
        self.fields['principal_remainder'].initial = self.loan.principal_remainder
        self.fields['principal_remainder'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        principal_remainder = float(self.cleaned_data['principal_remainder'])
        if not self.cleaned_data['accounts'] == 'Cash deposit':
            account = Account.objects.get(pk=self.cleaned_data['accounts'])
            if principal_remainder > account.available_balance:
                self.add_error('principal_remainder', 'Account balance is not enough to make payment!')

        return self.cleaned_data

    class Meta:
        model = BankLoan
        fields = ('principal_remainder',)
