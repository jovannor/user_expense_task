from rest_framework import serializers
from accounts import models as acc_models
from django.utils import timezone
from decimal import *

class UserSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = acc_models.User
        fields = ['id', 'username', 'email', 'created_at', 'balance', 'transactions']

    def get_transactions(self, obj):
        return {
            'incomes': obj.income_count or 0,
            'expenses': obj.expense_count or 0
        }


class IncomeSerializer(serializers.ModelSerializer):
    card = serializers.ChoiceField(choices=acc_models.Income.CARD)

    class Meta:
        model = acc_models.Income
        fields = ['id', 'amount', 'user_balance', 'date', 'card']
        read_only_fields = ['user_balance', 'date']
        extra_kwargs = {
            'amount': {'min_value': Decimal(1), 'max_value': Decimal(10000)},
        }


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(
        choices=acc_models.Expense.CATEGORY,
        default=acc_models.Expense.OTHER
    )

    class Meta:
        model = acc_models.Expense
        fields = ['id', 'amount', 'user_balance', 'date', 'category']
        read_only_fields = ['user_balance', 'date']
        extra_kwargs = {
            'amount': {'min_value': 1, 'max_value': 10000},
        }


class TransHistoryIncomeSerializer(serializers.ModelSerializer):
    trans_type = serializers.SerializerMethodField()

    class Meta:
        model = acc_models.Income
        fields = ['id', 'amount', 'user_balance', 'date', 'card', 'trans_type']
        read_only_fields = ['trans_type']

    def get_trans_type(self, obj):
        return obj.get('trans_type')


class TransHistoryExpenseSerializer(serializers.ModelSerializer):
    trans_type = serializers.SerializerMethodField()

    class Meta:
        model = acc_models.Expense
        fields = ['id', 'amount', 'user_balance', 'date', 'category', 'trans_type']

    def get_trans_type(self, obj):
        return obj.get('trans_type')
