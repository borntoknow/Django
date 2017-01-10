from django.db import models


class CarName (models.Model):
    name = models.CharField(max_length=50)


class Year (models.Model):
    name = models.CharField(max_length=10)


class BodyType (models.Model):
    name = models.CharField(max_length=50)


class Car (models.Model):
    car_name = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    mileage = models.CharField(max_length=6)
    pic_url = models.CharField(max_length=50)



