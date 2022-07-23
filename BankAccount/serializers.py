from rest_framework import serializers
from .models import CustomerAccount, BankTransaction, Bank

class CreateCustomerAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomerAccount
        fields = ('accountName', 'password')
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active=True
        instance.save()
        return instance
        

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankTransaction
        fields = '__all__'

class CreateBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'