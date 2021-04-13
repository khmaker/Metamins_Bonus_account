# Generated by Django 3.2 on 2021-04-13 15:11

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Номер телефона')),
                ('card_number', models.CharField(max_length=16, unique=True, verbose_name='Номер карты')),
                ('balance', models.PositiveIntegerField(default=0, verbose_name='Баланс')),
                ('created', models.DateTimeField(blank=True)),
                ('modified', models.DateTimeField(blank=True)),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунты',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('account creation', 'Account Creation'), ('money transfer', 'Money Transfer'), ('bonus transfer', 'Bonus Transfer')], max_length=50, verbose_name='Тип операции')),
                ('bonus_operation_type', models.CharField(choices=[('add bonus', 'Add Bonus'), ('subtract bonus', 'Subtract Bonus'), ('keep bonus', 'Keep Bonus')], max_length=50, verbose_name='Операция с бонусами')),
                ('amount', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(blank=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation', to='Bonus_account.account', verbose_name='Аккаунт')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
            },
        ),
    ]