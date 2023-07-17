from django.urls import path

from . import views

app_name = "mac"
urlpatterns = [
    path("", views.index, name="index"),
    path("contact_us/", views.contact_us, name="contact_us"),
    path("reminder/", views.reminder, name="reminder"),
    path("area_list/", views.AreaListView.as_view(), name="area_list"),
    path("area/<int:pk>", views.AreaDetailView.as_view(), name="area_detail"),
    path("restaurant_list/", views.RestaurantListView.as_view(), name="restaurant_list"),
    path("restaurant/<int:pk>", views.RestaurantDetailView.as_view(), name="restaurant_detail"),
    path("product_list/", views.ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
    path("dish_list/", views.DishListView.as_view(), name="dish_list"),
    path("dish/<int:pk>", views.DishDetailView.as_view(), name="dish_detail"),
    path("dish_create/", views.DishCreateView.as_view(), name="dish_create"),
    path("dish/<int:pk>/update/", views.DishUpdateView.as_view(), name="dish_update"),
    path("dish/<int:pk>/delete/", views.DishDeleteView.as_view(), name="dish_delete"),
]
