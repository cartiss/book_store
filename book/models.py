from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=300, verbose_name="Book name")
    price = models.PositiveIntegerField()
    author = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}: {self.name}'