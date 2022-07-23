from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, accountNumber, accountName, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(accountName, accountNumber, password, **other_fields)

    def create_user(self, accountName, accountNumber, password, **other_fields):

        if not accountName:
            raise ValueError(_('You must provide an account name'))

        user = self.model(accountName=accountName, accountNumber=accountNumber, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomerAccount(AbstractBaseUser, PermissionsMixin):

    accountNumber = models.CharField(validators=[MinLengthValidator(10)], max_length=10, unique=True)
    accountName = models.CharField(max_length=150, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    token = models.TextField(blank=True)
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'accountNumber'
    REQUIRED_FIELDS = ['accountName']

    def __str__(self):
        return self.accountName