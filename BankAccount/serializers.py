from decimal import Decimal
from rest_framework import serializers
from .models import CustomerAccount, BankTransaction, Bank
import random, string

def random_account_number():
    return ''.join(random.choice(string.digits) for _ in range(10))

class CreateCustomerAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomerAccount
        fields = ('accountName', 'password', 'initialDeposit', 'accountNumber')
        extra_kwargs = {'password': {'write_only':True}, 'accountNumber':{'read_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        #setting the account number
        instance.accountNumber = random_account_number()

        if password is not None:
            instance.set_password(password)
        instance.is_active=True
        instance.save()
        return instance
        

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankTransaction
        fields = ('balance',)

class GetAccountInfo(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'

class GetAccountStatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankTransaction
        fields = '__all__'

class CreateBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankTransaction
        fields = ('beneficiaryAccountNumber', 'Amount')

class WithdrawalSerializer(serializers.ModelSerializer):
    # withdrawnAmount = serializers.DecimalField(max_digits=30, decimal_places=2, default=Decimal(0.00))
    # accountNumber = serializers.CharField(max_length=10)

    class Meta:
        model = Bank
        fields = ('accountNumber', 'balance')
        # extra_kwargs = {'withdrawnAmount':{'read_only':True}}

    # def create(self, validated_data):
    #     withdrawnAmount = validated_data.pop('withdrawnAmount', None)
    #     accountNumber = validated_data.pop('accountNumber', None)
    #     instance = self.Meta.model(**validated_data)
    #     instance.save()

    #     return instance
        
    # def update(self, instance, validated_data):
    #     instance.withdrawnAmount = validated_data.get('withdrawnAmount', instance.withdrawnAmount)
    #     instance.accountNumber = validated_data.get('accountNumber', instance.accountNumber)
    #     instance.save()

    #     return instance

    