from django.urls import path
from .views import *

app_name = 'BankAccount'

urlpatterns = [
    path('', RegisterAccount.as_view, name='register' )
]