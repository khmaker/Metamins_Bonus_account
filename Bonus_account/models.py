# coding=utf-8
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import PositiveIntegerField
from django.db.models import PROTECT
from django.db.models import TextChoices
from django.db.models import DateTimeField
from phonenumber_field.modelfields import PhoneNumberField

from .errors import InvalidAmount
from .errors import InsufficientFunds


class Account(Model):
    first_name = CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя'
    )
    last_name = CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия'
    )
    phone_number = PhoneNumberField(
        blank=False,
        unique=True,
        verbose_name='Номер телефона'
    )
    card_number = CharField(
        max_length=16,
        blank=False,
        unique=True,
        verbose_name='Номер карты',
    )
    balance = PositiveIntegerField(
        default=0,
        verbose_name='Баланс',
    )
    created = DateTimeField(
        blank=True,
    )
    modified = DateTimeField(
        blank=True,
    )

    @classmethod
    def create(cls, first_name, last_name, phone_number, card_number, date):
        with transaction.atomic():
            account = cls.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                card_number=card_number,
                created=date,
                modified=date,
            )
            operation = Operation.create(
                account=account,
                amount=0,
                transaction_type=Operation.TransactionType.account_creation,
                date=date
            )
            return account, operation

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Operation(Model):
    class TransactionType(TextChoices):
        account_creation = 'account creation'
        money_transfer = 'money transfer'
        bonus_transfer = 'bonus transfer'

    class BonusOperationType(TextChoices):
        add_bonus = 'add bonus'
        subtract_bonus = 'subtract bonus'
        keep_bonus = 'keep bonus'

    transaction_type = CharField(
        max_length=50,
        choices=TransactionType.choices,
        verbose_name='Тип операции',
    )
    bonus_operation_type = CharField(
        max_length=50,
        choices=BonusOperationType.choices,
        verbose_name='Операция с бонусами',
    )
    amount = PositiveIntegerField(
        default=0
    )
    account = ForeignKey(
        Account,
        on_delete=PROTECT,
        related_name='operation',
        verbose_name='Аккаунт',
    )
    created = DateTimeField(
        blank=True,
    )

    @classmethod
    def create(
        cls,
        account,
        amount,
        transaction_type,
        date,
        bonus_operation_type=None
    ):
        if all([transaction_type == cls.TransactionType.bonus_transfer,
                bonus_operation_type is None]):
            e = {
                'bonus_operation_type':
                    f'required for {cls.TransactionType.bonus_transfer}'
            }
            raise ValidationError(e)
        if bonus_operation_type is None:
            bonus_operation_type = cls.BonusOperationType.keep_bonus
        return cls.objects.create(
            account=account,
            amount=amount,
            transaction_type=transaction_type,
            created=date,
            bonus_operation_type=bonus_operation_type
        )

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
