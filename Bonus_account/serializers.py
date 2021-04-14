# coding=utf-8
from rest_framework.serializers import ModelSerializer

from .models import Account
from .models import Operation


class AccountSerializer(ModelSerializer):
    def create(self, validated_data):
        account = Account.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number')
            )
        return account

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'card_number'
            )
        read_only_fields = ('card_number',)
        model = Account
        lookup_field = ('card_number', )


class OperationSerializer(ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'
