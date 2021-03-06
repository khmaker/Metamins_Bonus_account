# Комментарии о ходе разработки

Поскольку ранее с биллингом сталкиваться не приходилось, поискал варианты реализации и нашел [такой](https://hakibenita.com/bullet-proofing-django-models).
Хотелось реализовать подход с толстыми моделями и тонкими контроллерами.

## Модель бонусного аккаунта
Первое на что упал взгляд &mdash; поле с номером телефона. Довольно быстро нашлось [решение](https://github.com/stefanfoulis/django-phonenumber-field) для валидации телефонных номеров.
Далее я реализовал генератор номеров бонусных карт 
```python
from uuid import uuid4


def card_number_generator(length=16):
    return str(uuid4().int)[:length] if length <= 38 else None
```
и механизм их присвоения в методе класса модели, который проверят номера карт существующих аккаунтов и уже удаленных, проверяя номера карт в транзакциях.
```python
card_number_exists_in_base = True
card_number = None
while card_number_exists_in_base:
    card_number = card_number_generator(CARD_NUMBER_LENGTH)
    accounts = cls.objects.filter(card_number=card_number)
    operations = Operation.objects.filter(card_number=card_number)
    card_number_exists_in_base = any((accounts.exists(),
                                        operations.exists()))
```
Сверх требуемых полей были добавлены временны&#769;е метки для создания и изменения данных аккаунта. Последняя нужна для реализации сортировки аккаунтов по дате последней активности.
Количество бонусов является вычисляемым полем. Я успел понять что данная практика не является хорошей, но агрегация данных всех транзакций аккаунта, особенно при запросе данных всех аккаунтов, может негативно сказаться на времени быстродействия запросов. Реализация кэша данных заняла бы у меня непределенное время на разработку, поэтому баланс меняется после каждой транзакции и хранится в модели.

В модели реализованы методы создания аккаунта и операций с бонусами. Реализованы обработчики ошибок неверной величины списания и превышения лимита.

## Модель транзакции

Для транзакций доступно три типа:
* создание аккаунта
* операция с деньгами
* операция с бонусами

Также есть три типа операций с бонусами на случай, если при операциях с деньгами понадобится осуществлять какие-то операции с бонусами:
* начисление
* списание
* сохранение

Помимо связи с аккаунтом через внешний ключ в каждой транзакции хранится номер карты. Это необходимо для сохранения транзакций при удалении аккаунта и возможности отфильтровать их по номеру карты.