from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import User, Income, Expense


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0


class IncomeInline(admin.TabularInline):
    model = Income
    extra = 0


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_admin', 'is_active', 'balance', 'expense_count', 'income_count')
    list_filter = ('is_admin', 'is_admin',)
    search_fields = ('username', 'id', 'email')
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'password',
                ('is_admin', 'is_active', 'is_superuser',),
                'balance',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'balance', 'email', 'password', 'password_confirmation')}
         ),
    )
    ordering = ('-id',)
    filter_horizontal = ()
    inlines = [ExpenseInline, IncomeInline]

    @admin.display(description='Income')
    def income_count(self, obj):
        return Income.objects.filter(user=obj).count()

    @admin.display(description='Expense')
    def expense_count(self, obj):
        return Expense.objects.filter(user=obj).count()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

