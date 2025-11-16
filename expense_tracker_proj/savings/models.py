from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Saving(models.Model):
    CATEGORY_CHOICES = [
        ('Emergency Fund', 'Emergency Fund'),
        ('Travel', 'Travel'),
        ('Education', 'Education'),
        ('Investment', 'Investment'),
        ('Others', 'Others'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
