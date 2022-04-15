from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from BankOfSoftUni.auth_app.models import Profile

UserModel = get_user_model()


# Create your tests here.
class ProfileTest(django_test.TestCase):
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

    def test_create_profile(self):
        user = UserModel.objects.create_user(**self.USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.PROFILE_DATA,
            user=user,
        )

        return profile