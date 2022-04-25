from django.contrib import admin
# Register your models here.
from BankOfSoftUni.auth_app.models import Profile, BankUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'employee_role')
    list_filter = ('employee_role',)


@admin.register(BankUser)
class BankUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined')
    filter_horizontal = ('groups', 'user_permissions',)
    ordering = ('date_joined',)

