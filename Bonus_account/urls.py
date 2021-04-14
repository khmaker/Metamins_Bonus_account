# coding=utf-8
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AccountsViewSet
from .views import CreateAccountView
from .views import OperationsViewSet

v1_router = DefaultRouter()
v1_router.register(
    'accounts',
    AccountsViewSet,
    basename='accounts')
v1_router.register(
    r'accounts/(?P<card_number>[0-9]{16})/operations',
    OperationsViewSet,
    basename='operations')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/create_account', CreateAccountView.as_view()),
    ]
