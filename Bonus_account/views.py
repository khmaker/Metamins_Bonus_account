# coding=utf-8
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Account
from .serializers import AccountSerializer
from .serializers import OperationSerializer


class CreateAccountView(APIView):
    http_method_names = ('post', )

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        account = serializer.data
        return Response(
            data={'account': account},
            status=status.HTTP_201_CREATED)


class AccountsViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'card_number'
    http_method_names = ('get', )


class OperationsViewSet(ModelViewSet):
    serializer_class = OperationSerializer
    http_method_names = ('get',)

    def get_queryset(self):
        account = get_object_or_404(
            Account,
            card_number=self.kwargs.get('card_number'))
        return account.operation.all()
