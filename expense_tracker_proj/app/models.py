from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('Food & Groceries', 'Food & Groceries'),
        ('Transportation', 'Transportation'),
        ('Rent & Utilities', 'Rent & Utilities'),
        ('Health & Fitness', 'Health & Fitness'),
        ('Entertainment', 'Entertainment'),
        ('Shopping', 'Shopping'),
        ('Education', 'Education'),
        ('Travel', 'Travel'),
        ('Savings & Investments', 'Savings & Investments'),
        ('Miscellaneous', 'Miscellaneous'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Miscellaneous')

    def __str__(self):
        return f"{self.title} - {self.amount}"
