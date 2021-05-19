from django.db import models

class users_data (models.Model):
    Name = models.CharField(max_length=25)
    Gender = models.CharField(max_length=10)
    Email = models.EmailField()
    Contact = models.IntegerField()
    Password = models.CharField(max_length=20)
    Locality = models.CharField(max_length=20)


class shops_data(models.Model):
    Name = models.CharField(max_length=25)
    Gender = models.CharField(max_length=10)
    Shopname = models.CharField(max_length=50)
    Service = models.CharField(max_length=15)
    Email = models.EmailField()
    Contact = models.IntegerField()
    Password = models.CharField(max_length=20)
    Locality = models.CharField(max_length=20)

class shop_service (models.Model):
    Email = models.EmailField()
    Service = models.CharField(max_length=25)
    Price = models.CharField(max_length=5)
