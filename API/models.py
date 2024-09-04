from django.db import models

# Create your models here.
class Car(models.Model):
    car_brand=models.CharField(max_length=50)
    car_model=models.CharField(max_length=20)
    engin_type=models.CharField(max_length=20)
