from http import client
from rest_framework.views import APIView, status
from django.test import Client, TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from BankAccount.models import CustomerAccount

class TestCreateAccount(APITestCase):

    def authenticate_user(self):
        user = CustomerAccount.objects.create(accountName="Paystack Bank", password="tiseosinaike", initialDeposit=150000)

        # self.api_client=APIClient()
        # sample_request={
        #     "accountNumber":"5120656501",
        #     "accountPassword":"tiseosinaike"
        # }
        # register_request = {"accountName":"Flutterwave Bank", "accountPassword": "tiseosinaike","initialDeposit":150000}
        # self.client.post(reverse('bank:register'), register_request)
        # response = self.api_client.post(reverse('bank:login'), sample_request)
        # token = response.json()
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
        self.client.force_authenticate(user)
        

    def test_create_account(self):
        client=APIClient()
        previous_customer_count = CustomerAccount.objects.all().count()
        sample_request = {"accountName":"Stripes Bank", "accountPassword": "tiseosinaike","initialDeposit":15000}
        response = client.post(reverse('bank:register'), sample_request)
        self.assertEqual(CustomerAccount.objects.all().count(), previous_customer_count+1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_withdraw_endpoint(self):
        self.authenticate_user()
        sample_request = {
            "password":"tiseOsinaike",
            "accountNumber":"5120656501",
            "withdrawnAmount":5000
        }
        response = self.client.post(reverse('bank:withdraw'), sample_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_login_endpoint(self):
    #     user = CustomerAccount.objects.create(accountName="Paystack Bank", password="tiseosinaike", initialDeposit=150000, accountNumber=5120656501)
        
    #     login_request={
    #         "accountNumber":5120656501,
    #         "accountPassword":"tiseosinaike"
    #     }
    #     request=self.client.post(reverse('bank:login'), login_request)
        
    #     self.assertEqual(status.HTTP_200_OK, request.status_code)
        

        