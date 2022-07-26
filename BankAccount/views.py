from decimal import Decimal
import numbers
from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework import generics
from .models import Bank, BankTransaction, CustomerAccount
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CreateCustomerAccountSerializer, CreateBankSerializer, DepositSerializer, GetAccountInfo, GetAccountStatementSerializer, TransactionSerializer, WithdrawalSerializer
from django.utils.crypto import get_random_string
import random, string
from .models import BankTransaction
from rest_framework.permissions import AllowAny


class RegisterAccount(generics.CreateAPIView):
    permission_classes=[AllowAny]

    queryset = CustomerAccount.objects.all()
    serializer_class = CreateCustomerAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():

            #check if initial deposit is less than 500
            initial_deposit = Decimal(serializer.validated_data['initialDeposit'])
            if initial_deposit < 500.0:
                return Response({"Error":"Initial deposit should be #500 and above"}, status=status.HTTP_400_BAD_REQUEST)

            # print (serializer.data['accountName'], serializer.data['accountNumber'])
            user = serializer.save()
            
            token=RefreshToken.for_user(user).access_token
            user.token = token
            user.bankName = user.accountName
            user.save()
            
            #user already has a bank account
            Bank.objects.filter(customer=user).update(balance=user.initialDeposit,
             bankName = user.accountName, accountNumber=user.accountNumber, accountName=user.accountName)
            
            if user:
                return Response({'success':True, 'message':f'Account created successfully {serializer.data}'}, status=status.HTTP_200_OK)
        return Response({'success':False, 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class BlacklistTokenUpdateView(APIView):
    # the reason we are blacklisting is that when the user logs out we have to black list the refresh token.
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("You are logged out", status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # here we are extending the serializer class by customizing the token.
    @classmethod
    def get_token(cls, user):
        #get the token of the user by overwriting the function in the class
        token = super().get_token(user)
        #Add custom claims
        token['accountNumber']=user.accountNumber
        token['is_staff']=user.is_staff
        token['is_active']=user.is_active
        return token

class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class GetAccountInfo(generics.RetrieveAPIView):
    queryset = Bank
    serializer_class = GetAccountInfo
    def get(self, request, accountNumber, password):
        accountDetails=get_object_or_404(self.queryset, accountNumber=accountNumber)
        serializer = self.serializer_class(accountDetails)
        if accountDetails:
            return Response({'success':True,'message':'Get account statement successful', 'account':serializer.data}, status=status.HTTP_200_OK)
        return Response({'success':False, 'message':serializer.errors})

class GetAccountStatement(generics.RetrieveAPIView):
    queryset = Bank
    serializer_class = GetAccountStatementSerializer

    def get(self, request, accountNumber):
        accountStatement=get_object_or_404(self.queryset, accountNumber=accountNumber)
        serializer = self.serializer_class(accountStatement)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'success':False, 'message':serializer.errors})

class Deposit(generics.CreateAPIView):
    queryset = Bank
    serializer_class = DepositSerializer

    def post(self, request):

        #check for the right amount of money to be deposited
        amount = Decimal(request.data['amount'])
        
        if amount < 100.00 or amount > 1000000.00:
            return Response({'success':False, 'message':'Unable to deposit, amount exceeds a million naira or lower than hundred naira!!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            
            transactionDetails = serializer.save()

            beneficiaryAccount=get_object_or_404(self.queryset, accountNumber=transactionDetails.accountNumber)
            
            if beneficiaryAccount:
                beneficiaryAccount.balance+=transactionDetails.amount
                beneficiaryAccount.transactionType = transactionDetails.transactionType[0]
                beneficiaryAccount.bankName = beneficiaryAccount.bankName
                beneficiaryAccount.amount=transactionDetails.amount
                beneficiaryAccount.narration = f"{transactionDetails.transactionType[0]}" + 'ed'+ f" {transactionDetails.amount}"
                beneficiaryAccount.save()

            #save some details in the transaction table
            transactionDetails.transactionType = transactionDetails.transactionType[0]
            transactionDetails.bankName = beneficiaryAccount.bankName
            transactionDetails.narration = f"{transactionDetails.transactionType}"+ 'ed'+ f" {transactionDetails.amount}"
            transactionDetails.save()
            return Response({'success':True, 'message':f'You have credited this account {transactionDetails.accountNumber} with {transactionDetails.amount}'}, status=status.HTTP_200_OK)
        return Response({'success':False, 'message':serializer.errors})

class Withdrawal(generics.CreateAPIView):

    serializer_class = WithdrawalSerializer
    queryset=Bank

    def post(self, request):
        serializer= self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_account = serializer.save()

            bank = get_object_or_404(self.queryset, accountNumber=user_account['accountNumber'])
            amountLeft= user_account['withdrawnAmount']
            if bank:
                balance = bank.balance
                if balance-amountLeft<= 500.00:
                    return Response({"success":False,"message":"Unable to withdraw, insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)
                if balance-amountLeft <= 1.00:
                    return Response({"success":False,"message":"Unable to withdraw, insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)
                
                bank.balance-=user_account['withdrawnAmount']
                bank.transactionType = user_account['transactionType'][1]
                bank.amount=user_account['withdrawnAmount']
                bank.narration = f"{user_account['transactionType'][1]}" + ' of' f" {user_account['withdrawnAmount']}"
                bank.save()

                #create a transaction table for the withdrawal
                transaction = BankTransaction.objects.create(transactionType = user_account['transactionType'][1], bankName =bank.bankName,
                narration=f"{user_account['transactionType'][1]}"+ ' of'+ f" {user_account['withdrawnAmount']}", amount=user_account['withdrawnAmount'],accountNumber=bank.accountNumber )

                return Response({'success':True, 'message':'Your account has been debited with '+ str(user_account['withdrawnAmount'])+ ', left balance is '+f'{bank.balance}'}, status=status.HTTP_200_OK)

        return Response({'success':False, 'message':serializer.errors})