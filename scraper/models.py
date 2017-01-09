from django.db import models


class CarName (models.Model):
    name = models.CharField(max_length=50)


class Year (models.Model):
    name = models.CharField(max_length=10)


class BodyType (models.Model):
    name = models.CharField(max_length=50)


class Car (models.Model):
    car_name = models.ForeignKey('CarName')
    year = models.ForeignKey('Year')
    body_type = models.ForeignKey('BodyType')
    price = models.CharField(max_length=10)
    mileage = models.CharField(max_length=6)


