from django.db import models


class Brand (models.Model):
    text = models.CharField(max_length=50)
    value = models.CharField(max_length=5)


class Year (models.Model):
    text = models.CharField(max_length=4)
    value = models.CharField(max_length=4)


class BodyType (models.Model):
    name = models.CharField(max_length=50)
