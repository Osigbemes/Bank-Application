from rest_framework import serializers
from .models import CustomerAccount, BankTransaction, Bank

class CreateCustomerAccount(serializers.ModelSerializer):

    class Meta:
        model = CustomerAccount
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankTransaction
        fields = '__all__'

class CreateBank(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'