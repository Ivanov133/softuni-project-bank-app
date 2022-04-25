from django.contrib import admin
from django.utils.html import format_html

from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan


@admin.register(IndividualCustomer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer_number', 'full_name', 'ucn', 'document_number', 'annual_income', 'registration_date', 'id_card')
    list_filter = ('assigned_user', 'registration_date', 'gender', 'occupation',)
    ordering = ('registration_date',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'customer_id', 'available_balance', 'currency', 'open_date')
    list_filter = ('currency', 'open_date', 'customer_id',)
    ordering = ('open_date',)


@admin.register(BankLoan)
class BankLoanAdmin(admin.ModelAdmin):
    list_display = (
        'loan_number', 'principal', 'monthly_payment_value', 'currency', 'principal_remainder', 'duration_in_months',
        'interest_rate', 'next_monthly_payment_due_date', 'is_paid_monthly')
    list_filter = ('customer_debtor',)

    ordering = ('open_date',)
