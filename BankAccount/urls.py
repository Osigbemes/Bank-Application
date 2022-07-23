from django.urls import path
from .views import (BlacklistTokenUpdateView, RegisterAccount, MyTokenObtainPairView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'BankAccount'

urlpatterns = [
    path('create_account', RegisterAccount.as_view(), name='register'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]