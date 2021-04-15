# coding=utf-8
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Account
from .models import Operation
from .serializers import AccountSerializer
from .serializers import OperationSerializer

account_response = openapi.Response('response description', AccountSerializer)


class CreateAccountView(APIView):
    http_method_names = ('post', )

    @swagger_auto_schema(responses={201: account_response})
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        account = serializer.data
        return Response(
            data=account,
            status=status.HTTP_201_CREATED
            )


class AccountsViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'card_number'
    http_method_names = ('get',)


class OperationsViewSet(ModelViewSet):
    serializer_class = OperationSerializer
    http_method_names = ('get',)

    def get_queryset(self):
        return Operation.objects.filter(
            card_number=self.kwargs.get('card_number')
            )
