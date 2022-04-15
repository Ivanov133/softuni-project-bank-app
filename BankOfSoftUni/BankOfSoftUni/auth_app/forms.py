from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from BankOfSoftUni.helpers.validators import validate_only_letters

from BankOfSoftUni.auth_app.models import Profile


class CreateProfileForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        validators=(
            validate_only_letters,
        )
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
        validators=(
            validate_only_letters,)

    )
    profile_pic = forms.URLField()
    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            profile_pic=self.cleaned_data['profile_pic'],
            gender=self.cleaned_data['gender'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'profile_pic')
