from django.contrib.auth.models import User
from django.db import models

class Wallet(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Rs.{self.balance}"

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits = 10, decimal_places =2)
    type = models.CharField(max_length = 10) #credit/debit
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.type} ₹{self.amount} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"