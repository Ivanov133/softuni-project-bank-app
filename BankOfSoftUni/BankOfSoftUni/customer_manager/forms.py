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


# class AccountOpenForm(forms.ModelForm):
#     search_customer_by_ucn = forms.CharField(
#         max_length=30,
#     )
#
#     def __init__(self, user, *args, **kwargs):
#         super().__init__(user, *args, **kwargs)
#         self.user = user
#
#     def save(self, commit=True):
#         account = super().save(commit=False)
#         account.assigned_user = self.user
#
#         try:
#             customer = Customer.objects.get(pk=self.search_customer_by_ucn)
#         except:
#             raise ValidationError('Customer not found, please enter valid UCN')
#
#         account.customer = customer
#
#         if commit:
#             account.save()
#
#         return account
#
#     class Meta:
#         model = Account
#         fields = (
#             'currency',
#             'debit_card',
#         )


class AccountOpenForm(forms.ModelForm):
    # def __init__(self, user, customer, *args, **kwarg):
    #     self.user = user
    #     self.customer = customer
    #     super().__init__(*args, **kwarg)

    class Meta:
        model = Account
        fields = (
            'currency',
            'debit_card',
        )
