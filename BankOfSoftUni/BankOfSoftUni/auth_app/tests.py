from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from BankOfSoftUni.auth_app.models import Profile

UserModel = get_user_model()


class ProfileTestModel(django_test.TestCase):
    USER_CREDENTIALS = {
        'username': 'ST4884',
        'password': 'qweqwe',
    }

    PROFILE_DATA = {
        'first_name': 'Petar',
        'last_name': 'Ivanov',
        'gender': 'Male',
        'profile_pic': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
        'employee_role': 'Moderator',
    }

    def create_user(self):
        return UserModel.objects.create_user(**self.USER_CREDENTIALS)

    def test_create_profile_valid_data(self):
        user = self.create_user()
        profile = Profile.objects.create(
            **self.PROFILE_DATA,
            user=user,
        )

        self.assertEqual('Petar Ivanov', profile.full_name)
        self.assertEqual('Male', profile.gender)
        self.assertEqual('Moderator', profile.employee_role)
        self.assertIsNotNone(profile.pk)

    def test_create_profile_first_name_validator_invalid_data(self):
        user = self.create_user()
        invalid_first_name = 'Petar1'
        profile = Profile.objects.create(
            first_name=invalid_first_name,
            user=user,
            last_name=self.PROFILE_DATA['last_name'],
            gender=self.PROFILE_DATA['gender'],
            profile_pic=self.PROFILE_DATA['profile_pic'],
            employee_role=self.PROFILE_DATA['employee_role'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_create_profile_last_name_validator_invalid_data(self):
        user = self.create_user()
        invalid_last_name = 'Ivanov$'
        profile = Profile.objects.create(
            first_name=self.PROFILE_DATA['first_name'],
            user=user,
            last_name=invalid_last_name,
            gender=self.PROFILE_DATA['gender'],
            profile_pic=self.PROFILE_DATA['profile_pic'],
            employee_role=self.PROFILE_DATA['employee_role'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)


class ProfileTestView(django_test.TestCase):
    USER_CREDENTIALS = {
        'username': 'ST4884',
        'password': 'qweqwe',
    }

    PROFILE_DATA = {
        'first_name': 'Petar',
        'last_name': 'Ivanov',
        'gender': 'Male',
        'profile_pic': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
        'employee_role': 'Moderator',
    }

    def test_correct_template_render_register_user(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'users/create_user.html')

    def test_correct_template_render_edit_user(self):
        profile = Profile(
            **self.PROFILE_DATA,
            user=UserModel.objects.create_user(**self.USER_CREDENTIALS)
        )
        profile.save()
        response = self.client.get(reverse('profile edit', args=[profile.pk]))
        self.assertTemplateUsed(response, 'users/edit_profile.html')
