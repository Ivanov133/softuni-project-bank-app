from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.tasks_app.models import UserAnnualTargets

UserModel = get_user_model()


# Create your tests here.
class CustomerPanelTest(django_test.TestCase):
    USER_CREDENTIALS = {
        'username': 'ST4884',
        'password': 'qweqwe',
    }
    USER2_CREDENTIALS = {
        'username': 'ST45',
        'password': 'qweqwe',
    }
    PROFILE_DATA = {
        'first_name': 'Petar',
        'last_name': 'Ivanov',
        'gender': 'Male',
        'profile_pic': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
        'employee_role': 'Moderator',
    }
    VALID_CUSTOMER_DATA = {
        'first_name': 'Gosho',
        'sir_name': 'Petrov',
        'last_name': 'Petrov',
        'ucn': 8574859685,
        'document_number': 'HTASD554',
        'age': 45,
        'gender': 'Male',
        'annual_income': 15000,
        'occupation': 'Cashier',
        'date_of_birth': date(1997, 2, 17),
        'id_card': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
    }
    VALID_ACCOUNT_DATA = {
        'currency': 'BGN',
        'available_balance': 0,
        'debit_card': 'VISA',
    }
    VALID_LOAN_DATA = {
        'currency': 'BGN',
        'principal_remainder': 100000,
        'next_monthly_payment_due_date': date(2022, 2, 17),
        'duration_in_years': 15,
        'principal': 100000,
        'interest_rate': 5.5,
        'monthly_payment_value': 156.25,
    }
    VALID_TARGET_DATA = {
        'registered_clients_target': 20,
        'opened_accounts_target': 20,
        'opened_loans_count_target': 20,
        'total_loans_size_target': 200000,
    }

    def get_profile(self):
        user = UserModel.objects.create_user(**self.USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.PROFILE_DATA,
            user=user,
        )
        return profile

    def test_create_customer(self):
        user = UserModel.objects.create_user(**self.USER_CREDENTIALS)
        customer = IndividualCustomer.objects.create(
            **self.VALID_CUSTOMER_DATA,
            assigned_user=user,
        )
        return customer

    def test_create_account(self):
        user = UserModel.objects.create_user(**self.USER_CREDENTIALS)
        customer = IndividualCustomer.objects.create(
            **self.VALID_CUSTOMER_DATA,
            assigned_user=user,
        )
        account = Account.objects.create(
            **self.VALID_ACCOUNT_DATA,
            assigned_user=user,
            customer=customer,
        )

        return [user, account, customer]

    def test_create_loan(self):
        user, account, customer = self.test_create_account()
        loan = BankLoan.objects.create(
            **self.VALID_LOAN_DATA,
            customer_debtor=customer,
            account_credit=account,
            assigned_user=user,
        )
        return [user, account, customer, loan]

    def test_create_target_list(self):
        user = UserModel.objects.create_user(**self.USER2_CREDENTIALS)
        profile = Profile.objects.create(
            **self.PROFILE_DATA,
            user=user,
        )

        target_list = UserAnnualTargets.objects.create(
            **self.VALID_TARGET_DATA,
            profile=profile,
        )
        return target_list

    def test_if_target_list_is_updated(self):
        target_list = self.test_create_target_list()
        user, account, customer, loan = self.test_create_loan()

        self.assertEqual(1, target_list.opened_accounts_actual)
