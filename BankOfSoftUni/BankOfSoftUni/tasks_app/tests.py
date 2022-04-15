from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.tasks_app.models import UserAnnualTargets

UserModel = get_user_model()

class UserAnnualTargetsTest(django_test.TestCase):
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

    VALID_TARGET_DATA = {
        'registered_clients_target': 20,
        'opened_accounts_target': 20,
        'opened_loans_count_target': 20,
        'total_loans_size_target': 20,
    }

    def test_create_target_list(self):
        user = UserModel.objects.create_user(**self.USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.PROFILE_DATA,
            user=user,
        )

        target_list = UserAnnualTargets.objects.create(
            **self.VALID_TARGET_DATA,
            profile=profile,
        )

    