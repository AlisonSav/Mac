from django.db.models import Count
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from mac.models import Area, Dish, Product, Restaurant


def index(request):
    return render(request, "mac/index.html")


class AreaList(ListView):
    model = Area
    template_name = "mac/area_list.html"
    context_object_name = "area"

    def get_queryset(self):
        return Area.objects.all().annotate(restaurant_count=Count("restaurant__id"))


class AreaDetail(DetailView):
    model = Area

    def get_queryset(self):
        return Area.objects.select_related("restaurant")


class RestaurantList(ListView):
    model = Restaurant
    template_name = "mac/restaurant_list.html"
    context_object_name = "restaurant"

    def get_queryset(self):
        return Restaurant.objects.select_related("area").annotate(dish_count=Count("dish__id"))


class RestaurantDetail(DetailView):
    model = Restaurant

    def get_queryset(self):
        return Restaurant.objects.select_related("area").prefetch_related("dish_set__product").all()


class ProductList(ListView):
    model = Product
    template_name = "mac/product_list.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.all().annotate(dish_count=Count("dish__id"))


class ProductDetail(DetailView):
    model = Product

    def get_queryset(self):
        return Product.objects.prefetch_related("dish_set").all()


class DishList(ListView):
    model = Dish
    template_name = "mac/dish_list.html"
    context_object_name = "dish"

    def get_queryset(self):
        # return Restaurant.objects.prefetch_related("dish_set", "dish_set__product_set").annotate(
        #     dish_product_count=Count("product_set__product_id")
        # )  # something goes wrong...
        return Dish.objects.annotate(product_count=Count("product__id")).all()  # I get 151 SQL query
        # return Restaurant.objects.prefetch_related("dish_set").annotate(product_count=Count("product__id"))  # Can't
        # add annotate


class DishDetail(DetailView):
    model = Dish

    def get_queryset(self):
        return Dish.objects.select_related("restaurant").all()
