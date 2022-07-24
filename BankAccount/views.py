from decimal import Decimal
import numbers
from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView, status
from .models import Bank, BankTransaction, CustomerAccount
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CreateCustomerAccountSerializer, CreateBankSerializer, GetAccountInfo, TransactionSerializer
from django.utils.crypto import get_random_string
import random, string
from rest_framework.permissions import AllowAny

def generate_account_id():
    account_number = get_random_string(10, allowed_chars='0123456789')
    checkAccountNumber = CustomerAccount.objects.filter(accountNumber=account_number).exists()
    if not checkAccountNumber:
        return account_number
    generate_account_id()

# def random_account_number():
#     return ''.join(random.choice(string.digits) for _ in range(10))

class RegisterAccount(APIView):
    permission_classes=[AllowAny]

    queryset = CustomerAccount.objects.all()

    def post(self, request):
        serializer = CreateCustomerAccountSerializer(data=request.data)
        
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
                return Response({'success':True, 'message':f'Account created successfully {serializer.data}'}, status=status.HTTP_201_CREATED)
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
        # return Response({'success':True}, status=status.HTTP_201_CREATED)

class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class GetAccountInfo(APIView):
    queryset = Bank
    serializer_class = GetAccountInfo
    def get(self, request, accountNumber, password):
        accountDetails=get_object_or_404(self.queryset, accountNumber=accountNumber)
        serializer = self.serializer_class(accountDetails)
        if accountDetails:
            return Response({'success':True, 'message':serializer.data}, status=status.HTTP_200_OK)
        return Response({'success':False, 'message':serializer.errors})