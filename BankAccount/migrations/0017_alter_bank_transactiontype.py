# Generated by Django 3.2 on 2022-07-26 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankAccount', '0016_auto_20220726_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='transactionType',
            field=models.CharField(blank=True, choices=[('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal')], max_length=200, null=True),
        ),
    ]
