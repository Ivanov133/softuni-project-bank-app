from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from BankOfSoftUni.helpers.validators import validate_only_letters

from BankOfSoftUni.auth_app.models import Profile

# UserModel = get_user_model()

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
    # is_superuser = forms.ChoiceField(
    #     choices=[('True', 'True'), ('False', 'False')],
    # )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            profile_pic=self.cleaned_data['profile_pic'],
            gender=self.cleaned_data['gender'],
            # is_superuser=self.cleaned_data['is_superuser'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        # fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'profile_pic', 'is_superuser')

        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'profile_pic')
        # widgets = {
        #     'username': forms.TextInput(attrs={
        #         'class': "form-register-login",
        #         'placeholder': 'Enter Username'
        #     }),
        #     'password1': forms.TextInput(attrs={
        #         'class': "form-register-login",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Enter password'
        #     }),
        #     'password2': forms.TextInput(attrs={
        #         'class': "form-register-login",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Repeat password'
        #     }),
        #     'first_name': forms.TextInput(attrs={
        #         'class': "form-register-login",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Enter first name'
        #     }),
        #     'last_name': forms.TextInput(attrs={
        #         'class': "form-register-login",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Enter last name'
        #     }),
        #     'profile_pic': forms.TextInput(attrs={
        #         'class': "form-register-login",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'URL picture'
        #     }),
        # }
