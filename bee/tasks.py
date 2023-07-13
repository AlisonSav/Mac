import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.core.mail import send_mail
from django.template import loader

from bee.models import Quote, Author
from core import settings


@shared_task
def create_news():
    index_link = f"https://quotes.toscrape.com"
    page = 1
    while True:
        quotes_count = 0
        quote_dict = {}
        link = f"https://quotes.toscrape.com/page/{page}"
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        quotes = soup.findAll("div", class_="quote")
        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            author_link = quote.find("a").get("href")
            Author.objects.exists()
            if not Author.objects.filter(name=author).exists():
                about_author = requests.get(index_link + author_link)
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
                print(quote_dict)
                if quotes_count == 5:
                    Quote.objects.bulk_create(
                        Quote(quote=text, author_id=author) for text, author in quote_dict.items())
                    break
                if quotes_count == 0:
                    send_mail("No quotes",
                      loader.render_to_string("mac/template_email.html",
                                              {"message": "O no! You are have not any quotes"}),
                      settings.NOREPLY_EMAIL,
                      ["ohoho@ho.com"],
                      fail_silently=False)
                    break

        page += 1

