from django.core.validators import MinValueValidator
from django.db import models

from BankOfSoftUni.auth_app.models import BankUser, Profile


class UserAnnualTargets(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    registered_clients_target = models.IntegerField(
        validators=(
            MinValueValidator(0),
        )
    )

    registered_clients_actual = models.IntegerField(
        default=0,
        blank=True,
        null=True,
    )

    opened_accounts_target = models.IntegerField(
        validators=(
            MinValueValidator(0),
        )
    )

    opened_accounts_actual = models.IntegerField(
        default=0,
        blank=True,
        null=True,
    )

    opened_loans_count_target = models.IntegerField(
        validators=(
            MinValueValidator(0),
        )
    )

    opened_loans_actual = models.IntegerField(
        default=0,
        blank=True,
        null=True,
    )

    total_loans_size_target = models.FloatField(
        validators=(
            MinValueValidator(0),
        )
    )

    total_loans_size_actual = models.FloatField(
        default=0,
        blank=True,
        null=True,
    )

    @property
    def calc_customers_target_completion(self):
        target_tracker = (self.registered_clients_actual / self.registered_clients_target) * 100
        return f'{target_tracker :.2f}%'

    @property
    def calc_accounts_target_completion(self):
        target_tracker = (self.opened_accounts_actual / self.opened_accounts_target) * 100
        return f'{target_tracker :.2f}%'

    @property
    def calc_loans_count_target_completion(self):
        target_tracker = (self.opened_loans_actual / self.opened_loans_count_target) * 100
        return f'{target_tracker :.2f}%'

    @property
    def calc_loans_amount_target_completion(self):
        target_tracker = (self.total_loans_size_actual / self.total_loans_size_target) * 100
        return f'{target_tracker :.2f}%'

# TODO - Implement Non sales related tasks
# class UserTask(models.Model):
#     MAX_TASK_RESULT_LEN = 200
#     TASK_STATUSES = (
#         'Incomplete',
#         'Complete',
#     )
#     # Examples - need to be updated based ot products
#     TASK_TYPES = (
#         'Contact client and offer new loan type',
#         'Contact client and offer account with Debit card',
#         'Contact client and make an appointment',
#         'Contact client and remind of pending loan payments',
#         'Contact client and offer better loan deal with new interest rate',
#     )
#
#     assigned_user = models.ForeignKey(
#         BankUser,
#         on_delete=models.CASCADE,
#     )
#
#     assigned_customer = models.ForeignKey(
#         IndividualCustomer,
#         on_delete=models.CASCADE,
#     )
#     type = models.CharField(
#         max_length=80,
#         choices=[(x, x) for x in TASK_TYPES]
#     )
#
#     result = models.CharField(
#         max_length=MAX_TASK_RESULT_LEN,
#     )
#
#     end_date = models.DateTimeField()
#
#     created_date = models.DateTimeField(
#         auto_now_add=True,
#     )
#
#     status = models.CharField(
#         max_length=30,
#         default='Incomplete',
#         choices=[(x, x) for x in TASK_STATUSES]
#     )
