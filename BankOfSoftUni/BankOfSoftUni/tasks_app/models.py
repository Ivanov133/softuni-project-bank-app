from django.core.validators import MinValueValidator
from django.db import models

from BankOfSoftUni.auth_app.models import BankUser, Profile
from BankOfSoftUni.customer_manager.models import IndividualCustomer


class UserTask(models.Model):
    MAX_TASK_RESULT_LEN = 200
    TASK_STATUSES = (
        'Incomplete',
        'Complete',
    )

    TASK_TYPES = (
        'Register new client',
        'Open new account',
        'Open new loan',
    )

    assigned_user = models.ForeignKey(
        BankUser,
        on_delete=models.CASCADE,
    )

    type = models.CharField(
        max_length=30,
        choices=[(x, x) for x in TASK_TYPES]
    )

    result = models.CharField(
        max_length=MAX_TASK_RESULT_LEN,
    )

    end_date = models.DateTimeField()

    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    status = models.CharField(
        max_length=30,
        default='Incomplete',
        choices=[(x, x) for x in TASK_STATUSES]
    )

    # This is just for reference to the loan/account/customer number
    object_internal_number = models.CharField(
        max_length=30,
    )


class UserAnnualTargets(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
    )

    registered_clients = models.IntegerField(
        validators=(
            MinValueValidator(0),
        )
    )

    opened_accounts = models.IntegerField(
        validators=(
            MinValueValidator(0),
        )
    )

    opened_loans = models.IntegerField(
        validators=(
            MinValueValidator(0),
        )
    )
