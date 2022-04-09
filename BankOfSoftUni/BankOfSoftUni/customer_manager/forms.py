from django import forms
from django.core.exceptions import ValidationError

from BankOfSoftUni.customer_manager.models import Customer, Account


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
        model = Customer
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
            'date_of_birth': forms.SelectDateWidget(
                attrs={
                    'placeholder': 'Enter birth date',
                }
            ),

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
        model = Customer
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
            'date_of_birth': forms.SelectDateWidget(
                attrs={
                    'placeholder': 'Enter birth date',
                }
            ),

        }

