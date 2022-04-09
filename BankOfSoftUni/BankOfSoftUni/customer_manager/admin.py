from django.contrib import admin

# Register your models here.
from BankOfSoftUni.customer_manager.models import Customer, Account


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_number', 'full_name', 'ucn', 'registration_date',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'customer', 'available_balance', 'currency', 'open_date')
