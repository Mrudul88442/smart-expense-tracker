from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Target(models.Model):
    TARGET_TYPES = [
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
        ('3-5 Years', '3-5 Years'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_type = models.CharField(max_length=20, choices=TARGET_TYPES)
    target_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)  # ✅ this line fixed
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.title} ({self.goal_amount})"


