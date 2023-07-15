from bs4 import BeautifulSoup
import requests


def main():
    link = "https://quotes.toscrape.com/"
    page = 1
    r = requests.get(link + f"?page={page}")
    if r.status_code == 200:
        return

    soup = BeautifulSoup(r.text, "html.parser")
    pagination = soup.find("ul", class_="pagination")
    pages_count = len(pagination.find_all("li")) - 1

    l = []
    for i in range(pages_count):
        r = requests.get(link + f"?page={i + 1}")
        cards = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")
        for card in cards:
            l.append({"title": card.find("h4").get_text(strip=True),
                      "price": float(card.find("h5").get_text(strip=True)[1:])})
    print(l)
    for row in l:
        print(row)


if __name__ == "__main__":
    main()
