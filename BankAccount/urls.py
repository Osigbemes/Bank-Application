from django.urls import path
from .views import (BlacklistTokenUpdateView, Deposit, GetAccountStatement, RegisterAccount, Login, GetAccountInfo, Withdrawal)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'BankAccount'

urlpatterns = [
    path('create_account', RegisterAccount.as_view(), name='register'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('login/', Login.as_view(), name='token_obtain_pair'),
    path('deposit', Deposit.as_view(), name='deposit'),
    path('withdrawal', Withdrawal.as_view(), name='deposit'),
    path('account_info/<str:accountNumber>/<str:password>', GetAccountInfo.as_view(), name='get_account_info'),
    path('account_statement/<str:accountNumber>', GetAccountStatement.as_view(), name='get_account_statement'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]