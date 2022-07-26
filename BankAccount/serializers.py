from decimal import Decimal
from email.policy import default
from rest_framework import serializers
from .models import CustomerAccount, BankTransaction, Bank
import random, string

def random_account_number():
    return ''.join(random.choice(string.digits) for _ in range(10))

class CreateCustomerAccountSerializer(serializers.ModelSerializer):
    accountPassword = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomerAccount
        fields = ('accountName', 'accountPassword', 'initialDeposit', 'accountNumber')
        extra_kwargs = {'accountPassword': {'write_only':True}, 'accountNumber':{'read_only':True}}

    def create(self, validated_data):
        accountPassword = validated_data.pop('accountPassword', None)
        instance = self.Meta.model(**validated_data)

        #setting the account number
        instance.accountNumber = random_account_number()

        if accountPassword is not None:
            instance.set_password(accountPassword)
        instance.is_active=True
        instance.save()
        return instance
        

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankTransaction
        fields = ('balance',)

class GetAccountInfo(serializers.Serializer):
    accountName = serializers.CharField(max_length=150)
    accountNumber = serializers.CharField( max_length=10)
    balance = serializers.DecimalField(max_digits=30, decimal_places=2, default=Decimal(0.00))

    def create(self, validated_data):
        
        return validated_data

class GetAccountStatementSerializer(serializers.Serializer):
    TRANSACTIONTYPE=(
            ('Deposit', 'Deposit'),
            ('Withdrawal', 'Withdrawal')
        )

    transactionType = serializers.ChoiceField(choices=TRANSACTIONTYPE)
    transactionDate = serializers.DateTimeField()
    narration = serializers.CharField()
    amount = serializers.DecimalField(max_digits=30, decimal_places=2, default=Decimal(0.00))
    accountBalance = serializers.DecimalField(max_digits=30, decimal_places=2, default=Decimal(0.00))

    def create(self, validated_data):
        return validated_data

class CreateBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):
    TRANSACTIONTYPE=(
            ('Deposit', 'Deposit'),
            ('Withdrawal', 'Withdrawal')
        )

    transactionType = serializers.HiddenField(default=TRANSACTIONTYPE[0])

    class Meta:
        model = BankTransaction
        fields = ('accountNumber', 'amount', 'transactionType')

class WithdrawalSerializer(serializers.Serializer):
    TRANSACTIONTYPE=(
            ('Deposit', 'Deposit'),
            ('Withdrawal', 'Withdrawal')
        )
        
    transactionType = serializers.HiddenField(default=TRANSACTIONTYPE[1])
    withdrawnAmount = serializers.DecimalField(max_digits=30, decimal_places=2, default=Decimal(0.00))
    accountNumber = serializers.CharField(max_length=10)
    accountPassword = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        
        return validated_data

    