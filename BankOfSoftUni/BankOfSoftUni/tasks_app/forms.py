from django import forms

from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.tasks_app.models import UserAnnualTargets


class CreateTargetsForm(forms.ModelForm):
    class Meta:
        model = UserAnnualTargets
        fields = '__all__'


class EditTargetsForm(forms.ModelForm):
    class Meta:
        model = UserAnnualTargets
        fields = '__all__'


class DeleteTargetsForm(forms.ModelForm):
    class Meta:
        model = UserAnnualTargets
        fields = ()
