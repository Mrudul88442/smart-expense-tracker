from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class TransactionHistory(models.Model):
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
        ('Saving', 'Saving'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.transaction_type}: {self.title} - ₹{self.amount}"
