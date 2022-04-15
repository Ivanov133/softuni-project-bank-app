from django.contrib import admin

# Register your models here.
from BankOfSoftUni.tasks_app.models import UserAnnualTargets


@admin.register(UserAnnualTargets)
class UserAnnualTargetsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'calc_customers_target_completion', 'calc_loans_count_target_completion', 'calc_loans_amount_target_completion')