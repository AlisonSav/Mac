from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Prefetch
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.core.mail import send_mail
from django.conf import settings

from mac import tasks
from mac.models import Area, Dish, Product, Restaurant
from mac.forms import ContactForm, ReminderForm


def index(request):
    return render(request, "mac/index.html")


class AreaListView(ListView):
    model = Area
    template_name = "mac/area_list.html"
    context_object_name = "area"
    paginate_by = 20

    def get_queryset(self):
        return Area.objects.all().annotate(restaurant_count=Count("restaurant__id"))


class AreaDetailView(DetailView):
    model = Area

    def get_queryset(self):
        return Area.objects.select_related("restaurant")


class RestaurantListView(ListView):
    model = Restaurant
    template_name = "mac/restaurant_list.html"
    context_object_name = "restaurant"
    paginate_by = 20

    def get_queryset(self):
        return Restaurant.objects.select_related("area").annotate(dish_count=Count("dish__id"))


class RestaurantDetailView(DetailView):
    model = Restaurant

    def get_queryset(self):
        return Restaurant.objects.select_related("area").prefetch_related("dish_set__product").all()


class ProductListView(ListView):
    model = Product
    template_name = "mac/product_list.html"
    context_object_name = "product"
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.all().annotate(dish_count=Count("dish__id"))


class ProductDetailView(DetailView):
    model = Product

    def get_queryset(self):
        return Product.objects.prefetch_related("dish_set").all()


class DishListView(ListView):
    model = Dish
    context_object_name = "dish"
    paginate_by = 20

    def get_queryset(self):
        dishes_with_product_count = Dish.objects.annotate(product_count=Count("product__id"))
        r = Restaurant.objects.prefetch_related(Prefetch("dish_set", queryset=dishes_with_product_count))
        return dishes_with_product_count


class DishDetailView(DetailView):
    model = Dish

    def get_queryset(self):
        return Dish.objects.select_related("restaurant").all()


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    fields = ["dish_title", "for_who", "restaurant"]
    template_name = "mac/dish_create.html"
    success_message = "Dish created"


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    fields = ["dish_title", "for_who", "restaurant"]
    template_name = "mac/dish_update.html"
    success_message = "Dish updated"
    # messages.success(request, "Your profile was updated.")


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    success_url = reverse_lazy("mac:dish_list")
    success_message = "Dish deleted"


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
