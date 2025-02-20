from django.db import models
from datetime import datetime
from django.utils.timezone import now
# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE) 
    price = models.IntegerField()  
    quantity = models.IntegerField(null=True, default=1)

    def __str__(self):
      return self.product.name + " - $" +str(self.price)
    
class Register(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class OrderHistory(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    total_price = models.DecimalField(max_digits =10,decimal_places=2)
    purchased_at = models.DateTimeField(default=now)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Completed')

    def __str__(self):
        return f"Order {self.id} - {self.user.name} - {self.product.name} - {self.status}"

