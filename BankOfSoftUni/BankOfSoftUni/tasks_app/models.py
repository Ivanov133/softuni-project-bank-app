from django.db import models

from BankOfSoftUni.auth_app.models import BankUser
from BankOfSoftUni.customer_manager.models import IndividualCustomer


class UserTask(models.Model):
    TASK_TYPES = (
        'Register new client',
        'Open new account',
        'Open new loan',
    )

    assigned_user = models.ForeignKey(
        BankUser,
        on_delete=models.CASCADE,
    )

    assigned_customer = models.ForeignKey(
        IndividualCustomer,
        on_delete=models.CASCADE,
    )

    task_type = models.CharField(
        max_length=30,
        choices=[(x, x) for x in TASK_TYPES]
    )