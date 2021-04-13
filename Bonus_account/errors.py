# coding=utf-8

class Error(Exception):
    pass


class InvalidAmount(Error):

    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f'Invalid Amount: {self.amount}'


class InsufficientFunds(Error):

    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount

    def __str__(self):
        return f'amount: {self.amount}, current balance: {self.balance}'
