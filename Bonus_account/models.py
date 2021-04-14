# coding=utf-8
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import SET_NULL
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import PositiveIntegerField
from django.db.models import TextChoices
from phonenumber_field.modelfields import PhoneNumberField

from .errors import InsufficientFunds
from .errors import InvalidAmount

from .utils import card_number_generator


CARD_NUMBER_LENGTH = 16


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
        max_length=CARD_NUMBER_LENGTH,
        blank=False,
        unique=True,
        editable=False,
        verbose_name='Номер карты',
        )
    balance = PositiveIntegerField(
        default=0,
        verbose_name='Баланс',
        )
    created = DateTimeField(
        blank=True,
        verbose_name='Дата создания',
        )
    modified = DateTimeField(
        blank=True,
        verbose_name='Дата изменения',
        )

    @classmethod
    def create(cls, first_name, last_name, phone_number):
        card_number_exists_in_base = True
        card_number = None
        while card_number_exists_in_base:
            card_number = card_number_generator(CARD_NUMBER_LENGTH)
            accounts = cls.objects.filter(card_number=card_number)
            operations = Operation.objects.filter(card_number=card_number)
            card_number_exists_in_base = any((accounts.exists(),
                                              operations.exists()))
        with transaction.atomic():
            date = timezone.now()
            account = cls.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                card_number=card_number,
                created=date,
                modified=date,
                )
            Operation.create(
                account=account,
                amount=0,
                transaction_type=Operation.TransactionType.account_creation,
                date=date
                )
            return account

    @classmethod
    def add_bonus(
            cls,
            card_number,
            amount,
            ):
        if amount < 0:
            raise InvalidAmount(amount)
        with transaction.atomic():
            date = timezone.now()
            account = cls.objects.select_for_update().get(
                card_number=card_number
                )
            account.balance += amount
            account.modified = date
            account.save(update_fields=['balance', 'modified'])

            operation = Operation.create(
                account=account,
                amount=amount,
                transaction_type=Operation.TransactionType.bonus_transfer,
                date=date,
                bonus_operation_type=Operation.BonusOperation.add_bonus
                )
        return operation

    @classmethod
    def subtract_bonus(
            cls,
            card_number,
            amount,
            ):
        if amount < 0:
            raise InvalidAmount(amount)
        with transaction.atomic():
            date = timezone.now()
            account = cls.objects.select_for_update().get(
                card_number=card_number
                )
            if account.balance - amount < 0:
                raise InsufficientFunds(account.balance, amount)
            account.balance -= amount
            account.modified = date
            account.save(update_fields=['balance', 'modified'])

            operation = Operation.create(
                account=account,
                amount=amount,
                card_number=card_number,
                transaction_type=Operation.TransactionType.bonus_transfer,
                date=date,
                bonus_operation_type=Operation.BonusOperation.subtract_bonus
                )
        return operation

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ('-modified', )

    def __str__(self):
        return f'{self.card_number}'


class Operation(Model):
    class TransactionType(TextChoices):
        account_creation = 'account creation'
        money_transfer = 'money transfer'
        bonus_transfer = 'bonus transfer'

    class BonusOperation(TextChoices):
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
        choices=BonusOperation.choices,
        verbose_name='Операция с бонусами',
        )
    amount = PositiveIntegerField(
        default=0,
        verbose_name='Величина изменения',
        )
    account = ForeignKey(
        Account,
        on_delete=SET_NULL,
        null=True,
        related_name='operation',
        verbose_name='Аккаунт',
        )
    card_number = CharField(
        max_length=CARD_NUMBER_LENGTH,
        blank=False,
        editable=False,
        verbose_name='Номер карты',
        )
    created = DateTimeField(
        blank=True,
        verbose_name='Дата создания',
        )

    @classmethod
    def create(
            cls,
            account,
            amount,
            transaction_type,
            date=None,
            card_number=None,
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
            bonus_operation_type = cls.BonusOperation.keep_bonus
        date = timezone.now() if date is None else date
        number = account.card_number if card_number is None else card_number
        return cls.objects.create(
            account=account,
            amount=amount,
            transaction_type=transaction_type,
            created=date,
            card_number=number,
            bonus_operation_type=bonus_operation_type
            )

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
