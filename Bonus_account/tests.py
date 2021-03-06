# coding=utf-8
from json import loads

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from Bonus_account.models import Account


class AccountCreateTests(APITestCase):
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '9999999999'
        }

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('create_account')
        data = self.data.copy()
        response = self.client.post(url, data, format='json')
        account = Account.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(account.first_name, data.get('first_name'))
        self.assertEqual(account.last_name, data.get('last_name'))
        self.assertEqual(account.phone_number, data.get('phone_number'))
        self.assertIsNotNone(account.card_number)

    def test_create_account_with_missing_data(self):
        """
        Ensure we can't create a new account object without all necessary data.
        """
        url = reverse('create_account')
        data = self.data.copy()
        data.popitem()
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
            )
        self.assertEqual(Account.objects.count(), 0)

    def test_create_account_with_incorrect_data(self):
        """
        Ensure we can't create a new account object with incorrect data.
        """
        url = reverse('create_account')
        data = self.data.copy()
        data['phone_number'] = 'a386'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 0)

    def test_create_account_methods(self):
        """
        Ensure we can create a new account only with POST method.
        """
        url = reverse('create_account')
        data = self.data.copy()
        response_get = self.client.get(url, data, format='json')
        response_put = self.client.put(url, data, format='json')
        response_patch = self.client.patch(url, data, format='json')
        response_delete = self.client.delete(url, data, format='json')
        responses = (
            response_get, response_put, response_patch, response_delete,
            )
        for response in responses:
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )
        self.assertEqual(Account.objects.count(), 0)


class AccountsViewTests(APITestCase):
    accounts = []

    @classmethod
    def setUpTestData(cls):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '9876543210'
            }
        for suffix in range(10):
            phone_number = data['phone_number'] + str(suffix)
            account = Account.create(
                data['first_name'],
                data['last_name'],
                phone_number
                )
            cls.accounts.append(
                {
                    'first_name': account.first_name,
                    'last_name': account.last_name,
                    'phone_number': account.phone_number,
                    'card_number': account.card_number,
                    'balance': account.balance
                    }
                )

    def test_get_accounts_list(self):
        """
        Ensure we can get list of accounts
        """
        url = reverse('accounts-list')
        response = self.client.get(url)
        results = loads(response.content).get('results')
        self.assertEqual(results, self.accounts[::-1])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 10)

    def test_get_single_account(self):
        """
        Ensure we can get single account
        """
        for account in self.accounts:
            url = reverse('accounts-detail', kwargs={
                'card_number': account['card_number']
                })
            response = self.client.get(url)
            results = loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(results, account)
