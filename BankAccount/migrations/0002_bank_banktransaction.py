# Generated by Django 3.2 on 2022-07-23 13:43

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BankAccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionType', models.CharField(choices=[('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal')], max_length=200, null=True)),
                ('bankName', models.CharField(max_length=200)),
                ('Amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=30)),
                ('transactionDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('narration', models.TextField(blank=True)),
                ('accountNumber', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(10)])),
                ('beneficiaryAccountNumber', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(10)])),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankName', models.CharField(max_length=200)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=30)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]