from django_filters import rest_framework as filters
from accounts import models as acc_models


class ExpenseFilter(filters.FilterSet):
    category = filters.ChoiceFilter(choices=acc_models.Expense.CATEGORY)
    ordering = filters.OrderingFilter(fields=('date',))
    start_date = filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = acc_models.Expense
        fields = ['category', 'start_date', 'end_date']


class CategoryExpenseFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category", lookup_expr='in', method='filter_categories')
    start_date = filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = acc_models.Expense
        fields = ['category', 'start_date', 'end_date']

    def filter_categories(self, queryset, name, value):
        choices = [c[0] for c in acc_models.Expense.CATEGORY]
        categories = [c.lower() for c in value.split(',') if c in choices]
        return queryset.filter(**{name + '__in': categories})

class IncomeFilter(filters.FilterSet):

    card = filters.ChoiceFilter(choices=acc_models.Income.CARD)
    ordering = filters.OrderingFilter(fields=('date',))
    start_date = filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = acc_models.Income
        fields = ['card', 'start_date', 'end_date']
