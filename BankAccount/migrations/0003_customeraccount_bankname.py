# Generated by Django 3.2 on 2022-07-23 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankAccount', '0002_bank_banktransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeraccount',
            name='bankName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]