# coding=utf-8
from uuid import uuid4


def card_number_generator(length=16):
    return str(uuid4().int)[:length] if length <= 38 else None
