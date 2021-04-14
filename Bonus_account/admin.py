# coding=utf-8
from django.contrib.admin import ModelAdmin
from django.contrib.admin import site

from .models import Account
from .models import Operation


class AccountAdmin(ModelAdmin):
    list_display = (
        'card_number',
        'first_name',
        'last_name',
        'phone_number',
        )
    search_fields = (
        'card_number',
        'last_name',
        'phone_number',
        )
    readonly_fields = (
        'card_number',
        'balance',
        'created',
        'modified',
        )

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False


class OperationAdmin(ModelAdmin):
    list_display = (
        'account',
        'transaction_type',
        'bonus_operation_type',
        'created',
        )
    list_filter = (
        'transaction_type',
        'bonus_operation_type',
        'created',
        )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


site.register(Account, AccountAdmin)
site.register(Operation, OperationAdmin)
