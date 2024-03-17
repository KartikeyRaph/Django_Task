from django.db import models
from django.contrib.auth.models import User


class GroceryItem(models.Model):
    item = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

class GroceryList(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(GroceryItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
