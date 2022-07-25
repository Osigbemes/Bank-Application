from decimal import Decimal
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
    bankName = models.CharField(max_length=200, null=True, blank=True)
    initialDeposit = models.DecimalField(null=True,max_digits=10, decimal_places=2, default=Decimal(0.00))
    token = models.TextField(blank=True)
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'accountNumber'
    REQUIRED_FIELDS = ['accountName']

    def __str__(self):
        return self.accountName

class Bank(models.Model):
    accountNumber = models.CharField(validators=[MinLengthValidator(10)], unique=True, max_length=10, null=True)
    bankName = models.CharField(max_length=200)
    accountName = models.CharField(max_length=150, unique=True, null=True)
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=Decimal(0.00))
    customer = models.OneToOneField(CustomerAccount, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.bankName#self.customer.accountName

class BankTransaction(models.Model):
    TRANSACTIONTYPE=(
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal')
    )

    transactionType=models.CharField(max_length=200, null=True, choices=TRANSACTIONTYPE)
    bankName = models.CharField(max_length=200)
    Amount = models.DecimalField(max_digits=30, decimal_places=2, default=Decimal(0.00))
    transactionDate = models.DateTimeField(default=timezone.now)
    narration = models.TextField(blank=True)
    accountNumber = models.CharField(validators=[MinLengthValidator(10)], max_length=10)
    beneficiaryAccountNumber = models.CharField(validators=[MinLengthValidator(10)], max_length=10)