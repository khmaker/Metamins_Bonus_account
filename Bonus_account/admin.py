# coding=utf-8
from django.contrib.admin import ModelAdmin
from django.contrib.admin import site

from .models import Account
from .models import Operation


class AccountAdmin(ModelAdmin):
    search_fields = ('card_number', 'last_name', 'phone_number')
    list_editable = ('first_name', 'last_name', 'phone_number')

    def has_delete_permission(self, request, obj=None):
        return True


class OperationAdmin(ModelAdmin):
    list_filter = ('transaction_type', 'bonus_operation_type', 'created')

    def has_delete_permission(self, request, obj=None):
        return False


site.register(Account, AccountAdmin)
site.register(Operation, OperationAdmin)
