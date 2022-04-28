from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

from django.urls import reverse

from BankOfSoftUni.auth_app.models import Profile
from BankOfSoftUni.customer_manager.models import IndividualCustomer, Account, BankLoan
from BankOfSoftUni.tasks_app.models import UserAnnualTargets

UserModel = get_user_model()

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
    'duration_in_months': 15,
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


class CustomerPanelTestModels(django_test.TestCase):
    @staticmethod
    def get_user1():
        return UserModel.objects.create_user(**USER_CREDENTIALS)

    @staticmethod
    def get_user2():
        return UserModel.objects.create_user(**USER2_CREDENTIALS)

    @staticmethod
    def get_profile(user):
        profile = Profile.objects.create(
            **PROFILE_DATA,
            user=user,
        )
        return profile

    def get_customer(self):
        customer = IndividualCustomer.objects.create(
            **VALID_CUSTOMER_DATA,
            assigned_user=self.get_user1(),
        )

        return customer

    def get_account(self):
        customer = self.get_customer()
        return Account.objects.create(
            **VALID_ACCOUNT_DATA,
            assigned_user=customer.assigned_user,
            customer=customer,
        )

    def test_create_customer(self):
        customer = self.get_customer()
        customer.save()
        self.assertIsNotNone(customer.pk)

        return customer

    def test_create_account(self):
        account = self.get_account()
        account.save()
        self.assertIsNotNone(account.pk)

    def test_create_loan(self):
        account = self.get_account()
        loan = BankLoan.objects.create(
            **VALID_LOAN_DATA,
            customer_debtor=account.customer,
            account_credit=account,
            assigned_user=account.assigned_user,
            duration_remainder_months=VALID_LOAN_DATA['duration_in_months'],
        )
        loan.save()
        self.assertIsNotNone(loan.pk)

    def get_target_list(self):
        target_list = UserAnnualTargets.objects.create(
            **VALID_TARGET_DATA,
            profile=self.get_profile(self.get_user2()),
        )

        return target_list


class CustomerPanelTestViewsRedirectNotLoggedUser(django_test.TestCase):
    def test_customer_register_error_message_if_not_logged_in(self):
        response = self.client.get(reverse('customer register'))
        context = response.context['error']
        self.assertEqual(context, 'User is not authenticated')

    def test_customer_edit_error_message_if_not_logged_in(self):
        response = self.client.get(reverse('customer edit', args=[1]))
        context = response.context['error']
        self.assertEqual(context, 'User is not authenticated')

    def test_error_loan_create_if_not_logged_in(self):
        response = self.client.get(reverse('loan create', args=[1]))
        context = response.context['error']
        self.assertEqual(context, 'User is not authenticated')

    def test_loan_edit_error_message_if_not_logged_in(self):
        response = self.client.get(reverse('loan edit', args=[1]))
        context = response.context['error']
        self.assertEqual(context, 'User is not authenticated')

    def test_loan_delete_error_message_if_not_logged_in(self):
        response = self.client.get(reverse('loan delete', args=[1]))
        context = response.context['error']
        self.assertEqual(context, 'User is not authenticated')

    def test_account_edit_error_message_if_not_logged_in(self):
        response = self.client.get(reverse('account edit', args=[1]))
        context = response.context['error']
        self.assertEqual(context, 'User is not authenticated')

    def test_account_delete_error_message_if_not_logged_in(self):
        response = self.client.get(reverse('account delete', args=[1]))
        context = response.context['error']
        self.assertEqual(context, 'User is not authenticated')


class CustomerPanelTestViewsContext(django_test.TestCase):
    @staticmethod
    def get_user1():
        user = UserModel.objects.create_user(**USER_CREDENTIALS)
        user.set_password('123qwe')
        user.save()
        return user

    @staticmethod
    def get_user2():
        return UserModel.objects.create_user(**USER2_CREDENTIALS)

    @staticmethod
    def get_profile(user):
        profile = Profile.objects.create(
            **PROFILE_DATA,
            user=user,
        )
        return profile

    def get_customer(self):
        customer = IndividualCustomer.objects.create(
            **VALID_CUSTOMER_DATA,
            assigned_user=self.get_user1(),
        )

        return customer

    def get_account(self, customer):
        return Account.objects.create(
            **VALID_ACCOUNT_DATA,
            assigned_user=customer.assigned_user,
            customer=customer,
        )

    def test_customer_details_view__when_accounts_and_loans_are_created(self):
        customer = self.get_customer()
        customer.save()
        account = self.get_account(customer)
        account.save()
        user = customer.assigned_user
        loan = BankLoan.objects.create(
            **VALID_LOAN_DATA,
            customer_debtor=customer,
            account_credit=account,
            assigned_user=user,
            duration_remainder_months=VALID_LOAN_DATA['duration_in_months'],
        )
        loan.save()
        self.client.login(username=user.username, password='123qwe')
        response = self.client.get(reverse('customer details', args=[customer.pk]))

        context_customer = response.context['customer']
        context_account = response.context['accounts']
        context_loan = response.context['loans']
        self.assertTrue(context_account)
        self.assertTrue(context_customer)
        self.assertTrue(context_loan)


