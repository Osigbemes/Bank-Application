from django.urls import path
from .views import (BlacklistTokenUpdateView, RegisterAccount, Login, GetAccountInfo)
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
    path('account_info/<str:accountNumber>/<str:password>', GetAccountInfo.as_view(), name='get_account_info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]