from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)
    phone_number = models.CharField(verbose_name="phone_name", max_length=12)
    comment = models.CharField(verbose_name="comment", max_length=350)

    def __str__(self):
        return self.phone_number
