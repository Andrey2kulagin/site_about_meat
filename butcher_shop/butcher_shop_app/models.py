from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
