from django.urls import path

from . import views

app_name = "mac"
urlpatterns = [
    path("", views.index, name="index"),
    path("area_list/", views.AreaList.as_view(), name="area_list"),
    path("area/<int:pk>", views.AreaDetail.as_view(), name="area_detail"),
    path("restaurant_list/", views.RestaurantList.as_view(), name="restaurant_list"),
    path("restaurant/<int:pk>", views.RestaurantDetail.as_view(), name="restaurant_detail"),
    path("product_list/", views.ProductList.as_view(), name="product_list"),
    path("product/<int:pk>", views.ProductDetail.as_view(), name="product_detail"),
    path("dish_list/", views.DishList.as_view(), name="dish_list"),
    path("dish/<int:pk>", views.DishDetail.as_view(), name="dish_detail"),
]
