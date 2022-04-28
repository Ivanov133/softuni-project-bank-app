from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.tasks_app.models import UserAnnualTargets

UserModel = get_user_model()


class UserAnnualTargetTestModel(django_test.TestCase):
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

    TARGET_DATA = {
        'registered_clients_target': 10,
        'registered_clients_actual': 1,
        'opened_accounts_target': 10,
        'opened_accounts_actual': 1,
        'opened_loans_count_target': 10,
        'opened_loans_actual': 1,
        'total_loans_size_target': 10,
        'total_loans_size_actual': 1,
    }

    def create_user(self):
        return UserModel.objects.create_user(**self.USER_CREDENTIALS)

    def test_create_target_list(self):
        user = self.create_user()
        profile = Profile.objects.create(
            **self.PROFILE_DATA,
            user=user,
        )
        targets = UserAnnualTargets(
            **self.TARGET_DATA,
            profile=profile,
        )

        targets.save()
        self.assertIsNotNone(targets.pk)

    def test_create_target_list_calculation_properties(self):
        user = self.create_user()
        profile = Profile.objects.create(
            **self.PROFILE_DATA,
            user=user,
        )
        targets = UserAnnualTargets(
            **self.TARGET_DATA,
            profile=profile,
        )

        targets.save()
        self.assertEqual('10.00%', targets.calc_customers_target_completion)
        self.assertEqual('10.00%', targets.calc_accounts_target_completion)
        self.assertEqual('10.00%', targets.calc_loans_count_target_completion)
        self.assertEqual('10.00%', targets.calc_loans_amount_target_completion)
