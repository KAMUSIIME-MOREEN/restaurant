from distutils.command.upload import upload
from email.policy import default
import imghdr
import imp
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=300, default="", blank=True, null=True)
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to="foods", default="/foods/default.jpg", blank=True, null = True)

    def __str__(self):
        return self.name

class Orders(models.Model):
    owner = models.ForeignKey(User, models.CASCADE)
    order = models.ForeignKey(Food, models.CASCADE)
    qty = models.IntegerField(default=1, blank=True, null=True)
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=200, default="", blank=True, null=True)
    date = models.DateField(default=timezone.now)
    confirmed =  models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner)
