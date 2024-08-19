from django.db import models
from django.contrib.auth.models import User

class CEO(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    company = models.CharField(max_length=255)
    tenure = models.IntegerField()
    education = models.CharField(max_length=255)
    previouse_companies = models.JSONField(default=list)
    compensation = models.DecimalField(max_digits=15, decimal_places=2)
    country_of_origin = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.company}"
    

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    ceo = models.OneToOneField(CEO, on_delete=models.SET_NULL, null=True, related_name='stock')
    sector = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)
    current_price = models.DecimalField(max_digits=15, decimal_places=2)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2)
    pe_ratio = models.DecimalField(max_digits=5, decimal_places=2)
    eps = models.DecimalField(max_digits=5, decimal_places=2)
    employees = models.IntegerField()

    def __str__(self):
        return f"{self.symbol} - {self.name}"
    

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchlist')
    stocks = models.ManyToManyField(Stock, related_name='watchlist')

    def __str__(self):
        return f"{self.user.username}'s Watchlist"