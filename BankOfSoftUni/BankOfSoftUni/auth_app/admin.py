from django.contrib import admin

# Register your models here.
from BankOfSoftUni.auth_app.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'employee_role')
