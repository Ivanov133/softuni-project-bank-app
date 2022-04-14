from django import forms

from BankOfSoftUni.tasks_app.models import UserAnnualTargets


class CreateTargetsForm(forms.ModelForm):
    class Meta:
        model = UserAnnualTargets
        fields = '__all__'
