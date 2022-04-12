from django.db import models

from BankOfSoftUni.auth_app.models import BankUser
from BankOfSoftUni.customer_manager.models import Customer


class UserTask(models.Model):
    # TASK_TYPES = (
    #     'Register new client',
    #     'Open new account',
    #
    # )
    #
    # assigned_user = models.ForeignKey(
    #     BankUser,
    #     on_delete=models.CASCADE,
    # )
    #
    # assigned_customer = models.ForeignKey(
    #     Customer,
    #     on_delete=models.CASCADE,
    # )
    #
    # task_type = models.CharField()
    pass
