from django.contrib import admin

from mac.models import Area, Dish, Product, Restaurant


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("area_title", "country")
    search_fields = ["area_title", "country"]
    list_per_page = 10


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("title", "size", "area")
    search_fields = ["title", "area"]
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_title", "energy")
    filter_horizontal = ["dish"]
    search_fields = ["product_title"]
    list_per_page = 10
    ordering = ["product_title"]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("dish_title", "for_who", "restaurant", "kids_status")
    filter_horizontal = ["product"]
    search_fields = ["dish_title", "restaurant"]
    list_per_page = 10
    fieldsets = [
        ("General information", {"fields": ["dish_title", "for_who"]}),
        ("Other information", {"fields": ["restaurant"]}),
    ]

    @admin.display(ordering="for_who", description="Status")
    def kids_status(self, dish: Dish):
        if dish.for_who == "FK":
            return "KIDS!"
