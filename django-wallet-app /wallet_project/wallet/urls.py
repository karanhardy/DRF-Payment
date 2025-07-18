from django.urls import path
from .views import RegisterView ,admin_dashboard, WalletTopUpView, WalletTransferView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
               path('register/', RegisterView.as_view(), name ='register'),
               path('login/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
               path('token/refresh/' , TokenRefreshView.as_view(), name = 'token_refresh'),
               path('admin-dashboard/' , admin_dashboard, name = 'admin-dashboard'),
               # path('' , dashboard, name = 'dashboard'),
               path('wallet/topup', WalletTopUpView.as_view(), name = 'wallet-topup'),
               path('wallet/transfer', WalletTransferView.as_view(),name = 'wallet-transfer'),
                ]
#syntax urlpatterns = [path('url/path/',views.view_function, name ='url-name')]

