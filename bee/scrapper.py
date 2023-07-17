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

    lst = []
    for i in range(pages_count):
        r = requests.get(link + f"?page={i + 1}")
        cards = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")
        for card in cards:
            lst.append({"title": card.find("h4").get_text(strip=True),
                        "price": float(card.find("h5").get_text(strip=True)[1:])})
    for row in lst:
        print(row)  # noqa: T201


if __name__ == "__main__":
    main()
