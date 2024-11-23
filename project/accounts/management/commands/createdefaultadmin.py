from decimal import Decimal
import random

from faker import Faker
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import User, Income, Expense


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(
                username=settings.DEFAULT_ADMIN_NAME,
                email=settings.DEFAULT_ADMIN_EMAIL,
                password=settings.DEFAULT_ADMIN_PASSWORD,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'*' * 4} Admin with email {settings.DEFAULT_ADMIN_EMAIL} has been created! {'*' * 4}"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'*'*4} Admin with such email {settings.DEFAULT_ADMIN_EMAIL} already exists! {'*'*4}"
                )
            )

        fake = Faker()

        for _ in range(20):
            user = User.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                is_active=True,
                password='qwerty123456!',
                balance=Decimal('0.00')
            )

            transactions_count = random.randint(10, 20)
            for _ in range(transactions_count):
                if random.choice([True, False]):
                    amount = Decimal(random.uniform(50.0, 1000.0)).quantize(Decimal('0.01'))
                    user.balance += amount

                    Income.objects.create(
                        user=user,
                        amount=amount,
                        user_balance=user.balance,
                        date=fake.date_between(start_date='-120d', end_date='today'),
                        card=random.choice([Income.VISA, Income.MASTERCARD])
                    )
                else:
                    amount = Decimal(random.uniform(10.0, 500.0)).quantize(Decimal('0.01'))
                    user.balance -= amount

                    Expense.objects.create(
                        user=user,
                        amount=amount,
                        user_balance=user.balance,
                        date=fake.date_between(start_date='-120d', end_date='today'),
                        category=random.choice(
                            [Expense.FOOD, Expense.TRAVEL, Expense.UTILITIES, Expense.OTHER])
                    )

            user.save()

        self.stdout.write(self.style.SUCCESS(f"{'*'*4} Successfully generated fake data! {'*'*4}"))
