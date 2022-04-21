from django import forms

from BankOfSoftUni.tasks_app.models import UserAnnualTargets


class CreateTargetsForm(forms.ModelForm):
    def save(self, commit=True):
        print('test')
    class Meta:
        model = UserAnnualTargets
        fields = '__all__'
