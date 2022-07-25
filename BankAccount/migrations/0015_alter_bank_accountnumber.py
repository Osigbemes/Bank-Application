# Generated by Django 3.2 on 2022-07-25 15:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankAccount', '0014_alter_bank_accountnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='accountNumber',
            field=models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]