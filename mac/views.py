from django.db.models import Count, Prefetch
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.core.mail import send_mail
from django.conf import settings

from mac import tasks
from mac.models import Area, Dish, Product, Restaurant
from mac.forms import ContactForm, ReminderForm


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
        dishes_with_product_count = Dish.objects.annotate(product_count=Count("product__id"))
        r = Restaurant.objects.prefetch_related(Prefetch("dish_set", queryset=dishes_with_product_count))
        return r


class DishDetail(DetailView):
    model = Dish

    def get_queryset(self):
        return Dish.objects.select_related("restaurant").all()


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data.get("subject"),
                loader.render_to_string("mac/template_email.html", {"message": form.cleaned_data.get("message")}),
                settings.NOREPLY_EMAIL,
                [form.cleaned_data.get("from_email")],
                fail_silently=False,
            )
            return redirect(reverse("mac:index"))
    else:
        form = ContactForm()
    return render(request, "mac/contact_us.html", {"form": form})


def reminder(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            subject = "Reminder"
            to_email = form.cleaned_data.get("to_email")
            message = form.cleaned_data.get("message")
            when = form.cleaned_data.get("when")
            tasks.send_remind.apply_async(kwargs={"subject": subject,
                                                  "message": loader.render_to_string("mac/remind_email.html",
                                                                                     {"message": message,
                                                                                      "subject": subject}),
                                                  "email": to_email}, eta=when)
            return redirect(reverse("mac:index"))
    else:
        form = ReminderForm()
    return render(request, "mac/reminder.html", {"form": form})
