from django.contrib import admin

from bee.models import Quote, Author


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("quote", "author")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "born_date", "born_loc", "about")
