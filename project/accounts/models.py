from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('The user must have an email')

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None):
        if username == "":
            username = None
        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, null=True, blank=True, max_length=300, verbose_name='Username')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_admin = models.BooleanField(default=False, verbose_name='Admin')
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username or self.email

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    user_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Income(Transaction):
    VISA = 'visa'
    MASTERCARD = 'mastercard'

    CARD = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard')
    ]

    user = models.ForeignKey(User, null=True, related_name='income_trans', on_delete=models.SET_NULL)
    card = models.CharField(max_length=10, choices=CARD)


class Expense(Transaction):
    FOOD = 'food'
    TRAVEL = 'travel'
    UTILITIES = 'utilities'
    OTHER = 'other'

    CATEGORY = [
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, null=True, related_name='expense_trans', on_delete=models.SET_NULL)
    category = models.CharField(max_length=10, choices=CATEGORY, default=OTHER)


