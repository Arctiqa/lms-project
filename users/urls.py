from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, \
    PaymentListAPIView, PaymentCreateAPIView, SubscriptionAPIView, PaymentAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('list/', UserListAPIView.as_view(), name='user-list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-get'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),

    path('payments/', PaymentListAPIView.as_view(), name='payments-list'),
    # path('payments/create/', PaymentCreateAPIView.as_view(), name='payments-create'),

    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
    path('payment/', PaymentAPIView.as_view(), name='payment')
]
