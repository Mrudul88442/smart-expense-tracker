from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    INCOME_CATEGORIES = [
        ('Salary', 'Salary'),
        ('Freelance', 'Freelance'),
        ('Investments', 'Investments'),
        ('Business', 'Business'),
        ('Rental Income', 'Rental Income'),
        ('Gifts', 'Gifts'),
        ('Bonuses', 'Bonuses'),
        ('Interest', 'Interest'),
        ('Savings Withdrawal', 'Savings Withdrawal'),
        ('Miscellaneous', 'Miscellaneous'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=INCOME_CATEGORIES)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
