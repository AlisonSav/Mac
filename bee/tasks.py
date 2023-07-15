import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.core.mail import send_mail

from bee.models import Quote, Author
from core import settings


@shared_task
def add_quote():
    BASE_URL = f"https://quotes.toscrape.com"
    page = 1
    quotes_count = 0
    quote_dict = {}
    while True:
        link = f"https://quotes.toscrape.com/page/{page}"
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        quotes = soup.findAll("div", class_="quote")
        if not soup("span", class_="text"):
            send_mail("No quotes",
                      "O no! You are have not any quotes",
                      settings.NOREPLY_EMAIL,
                      ["ohoho@ho.com"],
                      fail_silently=False)
            return
        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            author_link = quote.find("a").get("href")
            if not Author.objects.filter(name=author).exists():
                about_author = requests.get(BASE_URL + author_link)
                soup = BeautifulSoup(about_author.text, "html.parser")
                about = soup.findAll("div", class_="author-details")
                for a in about:
                    born = a.find("span", class_="author-born-date").text
                    loc = a.find("span", class_="author-born-location").text
                    desc = a.find("div", class_="author-description").text
                Author.objects.create(name=author, born_date=born, born_loc=loc, about=desc)
            author = Author.objects.get(name=author)
            if not Quote.objects.filter(quote=text).exists():
                quote_dict[text] = author.id
                quotes_count += 1
                if quotes_count == 5:
                    print(quote_dict)
                    Quote.objects.bulk_create(
                        Quote(quote=text, author_id=author) for text, author in quote_dict.items())
                    return
        page += 1
