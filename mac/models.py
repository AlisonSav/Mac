from django.db import models
from django.urls import reverse

SIZE_CHOICES = [
    ("S", "Small"),
    ("M", "Middle"),
    ("L", "Large"),
]

FOR_CHOICES = [
    ("F1", "For 1 person"),
    ("F2", "For 2 person"),
    ("FK", "For kids"),
]


class Area(models.Model):  # noqa: DJ10, DJ11
    area_title = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=20)

    def __str__(self):
        return f"Area: {self.area_title}, {self.country}"


class Restaurant(models.Model):  # noqa: DJ10, DJ11
    title = models.CharField(max_length=20)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    area = models.OneToOneField(Area, on_delete=models.CASCADE)

    def __str__(self):
        return f"Restaurant: {self.title}, {self.size}. {self.area}"


class Product(models.Model):  # noqa: DJ10, DJ11
    product_title = models.CharField(max_length=20)
    energy = models.IntegerField(default=0)

    def __str__(self):
        return f"Product: {self.product_title}, Energy: {self.energy}"


class Dish(models.Model):  # noqa: DJ10, DJ11
    dish_title = models.CharField(max_length=20)
    for_who = models.CharField(max_length=20, choices=FOR_CHOICES)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, blank=True, null=True
    )
    product = models.ManyToManyField(Product)

    def __str__(self):
        return f"Dish: {self.dish_title}, {self.for_who}, {self.restaurant}"

    def get_absolute_url(self):
        return reverse('mac:dish_detail', kwargs={'pk': self.pk})
