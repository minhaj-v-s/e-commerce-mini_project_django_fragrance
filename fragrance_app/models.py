from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name
    

    

