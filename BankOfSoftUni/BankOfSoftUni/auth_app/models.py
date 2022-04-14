from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from django.db import models

from BankOfSoftUni.auth_app.managers import BankUserManager
from BankOfSoftUni.helpers.validators import validate_only_letters, MaxFileSizeInMbValidator


class BankUser(auth_models.AbstractUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 30

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = 'username'

    objects = BankUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 40
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 40

    GENDERS = [(x, x) for x in ('Male', 'Female')]

    IMAGE_UPLOAD_DIR = 'profile_images'
    IMAGE_MAX_SIZE_IN_MB = 5

    EMPLOYEE_POSITIONS = [(x, x) for x in (
        'Cashier',
        'Credit consultant',
        'Branch manager',
        'Moderator',
    )]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    profile_pic = models.ImageField(
        upload_to=IMAGE_UPLOAD_DIR,
        null=True,
        blank=True,
        validators=(
            MaxFileSizeInMbValidator(IMAGE_MAX_SIZE_IN_MB),
        )
    )

    employee_role = models.CharField(
        max_length=max(len(x) for x, _ in EMPLOYEE_POSITIONS),
        choices=EMPLOYEE_POSITIONS,
    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
    )

    user = models.OneToOneField(
        BankUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.user.username}: {self.first_name} {self.last_name} - {self.employee_role}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

