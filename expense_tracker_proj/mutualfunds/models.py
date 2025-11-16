from django.db import models
from django.contrib.auth.models import User

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheme_code = models.CharField(max_length=50)
    scheme_name = models.CharField(max_length=255)
    units = models.FloatField()
    purchase_price = models.FloatField()
    purchase_date = models.DateField()

    def __str__(self):
        return f"{self.scheme_name} ({self.user.username})"

    @property
    def invested_value(self):
        return round(self.units * self.purchase_price, 2)
