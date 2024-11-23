from django.db.models import Count, Q, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from decimal import Decimal
from .serializers import (
    UserSerializer,
    IncomeSerializer,
    ExpenseSerializer, TransHistoryIncomeSerializer, TransHistoryExpenseSerializer,
)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from accounts import models as acc_models
from rest_framework.generics import get_object_or_404
from django.db import transaction, models
from accounts.filters import (
    ExpenseFilter,
    IncomeFilter,
    CategoryExpenseFilter
)


class UserRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = acc_models.User.objects.filter(is_admin=False).annotate(
                income_count=Count('income_trans', distinct=True),
                expense_count=Count('expense_trans', distinct=True)
            )

    def get_object(self):
        return get_object_or_404(queryset=self.queryset, id=self.kwargs.get('user_id'))


class UserListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = acc_models.User.objects.filter(is_admin=False).annotate(
                income_count=Count('income_trans', distinct=True),
                expense_count=Count('expense_trans', distinct=True)
            )
    serializer_class = UserSerializer


class UserTransactionsHistoryView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExpenseSerializer

    def get_user(self):
        return get_object_or_404(acc_models.User.objects.filter(is_admin=False), id=self.kwargs.get('user_id'))

    def get_queryset(self):
        user = self.get_user()
        income_qs = acc_models.Income.objects.filter(user=user).annotate(
            trans_type=models.Value('income', output_field=models.CharField())
        ).values('id', 'amount', 'date', 'user_balance', 'trans_type', 'card')

        expense_qs = acc_models.Expense.objects.filter(user=user).annotate(
            trans_type=models.Value('expense', output_field=models.CharField())
        ).values('id', 'amount', 'date', 'user_balance', 'trans_type', 'category')

        return income_qs.union(expense_qs).order_by('date')

    def serialize_objects(self, queryset):
        serialized_data = []
        for item in queryset:
            if item['trans_type'] == 'income':
                serialized_data.append(TransHistoryIncomeSerializer(item).data)
            elif item['trans_type'] == 'expense':
                serialized_data.append(TransHistoryExpenseSerializer(item).data)
        return serialized_data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.serialize_objects(page)
            return self.get_paginated_response(data)

        data = self.serialize_objects(queryset)
        return Response(data)


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter

    def get_user(self):
        return get_object_or_404(acc_models.User.objects.filter(is_admin=False), id=self.kwargs.get('user_id'))

    def get_queryset(self):
        user = self.get_user()
        return acc_models.Expense.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        user = self.get_user()
        with transaction.atomic():
            expense = serializer.save(user=user)
            user.balance -= expense.amount
            if user.balance < 0:
                raise ValidationError({"detail": "Insufficient funds."})
            expense.user_balance = user.balance
            expense.save()
            user.save()

    def perform_update(self, serializer):
        user = self.get_user()
        instance = self.get_object()

        with transaction.atomic():
            updated_instance = serializer.save()

            if updated_instance.amount != instance.amount:
                user.balance += instance.amount
                user.balance -= updated_instance.amount
                if user.balance < 0:
                    raise ValidationError({"detail": "Insufficient funds."})
                updated_instance.user_balance = user.balance
                updated_instance.save()
                user.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user

        with transaction.atomic():
            user.balance += instance.amount
            user.save()
            instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class IncomeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = IncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncomeFilter

    def get_user(self):
        return get_object_or_404(acc_models.User.objects.filter(is_admin=False), id=self.kwargs.get('user_id'))

    def get_queryset(self):
        user = self.get_user()
        return acc_models.Income.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        user = self.get_user()
        with transaction.atomic():
            income = serializer.save(user=user)
            user.balance += income.amount
            income.user_balance = user.balance
            income.save()
            user.save()

    def perform_update(self, serializer):
        user = self.get_user()
        instance = self.get_object()

        with transaction.atomic():
            updated_instance = serializer.save()
            if updated_instance.amount != instance.amount:
                user.balance -= instance.amount
                user.balance += updated_instance.amount
                serializer.save(user_balance=user.balance)
                user.save()
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user

        with transaction.atomic():
            user.balance -= instance.amount
            user.save()
            instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserExpenseCategorySumView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryExpenseFilter
    pagination_class = None

    def get_queryset(self):
        user = get_object_or_404(acc_models.User.objects.filter(is_admin=False), id=self.kwargs.get('user_id'))
        return acc_models.Expense.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        summary = queryset.aggregate(
            total=Sum('amount'),
            transaction_count=Count('id')
        )
        return Response(
            {
                'total_expense_amount': Decimal(summary['total'] or 0),
                'transaction_count': summary['transaction_count']
            }
        )

