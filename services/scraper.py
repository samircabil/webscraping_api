import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

BASE_URL = "https://books.toscrape.com/"


# HÄMTA OCH SPARA KATEGORIER

def get_categories():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "lxml")

    categories = []
    category_list = soup.find("ul", class_="nav-list").find_all("a")

    for cat in category_list:
        name = cat.text.strip()
        url = BASE_URL + cat["href"]

        if name != "Books":
            categories.append({
                "name": name,
                "url": url
            })

    return categories


def save_categories():
    categories = get_categories()

    os.makedirs("data", exist_ok=True)

    with open("data/categories.json", "w") as f:
        json.dump(categories, f, indent=4)

    return categories


def load_categories_from_file():
    if os.path.exists("data/categories.json"):
        with open("data/categories.json") as f:
            return json.load(f)

    return save_categories()


# VÄXELKURS

def get_exchange_rate():
    url = "https://www.x-rates.com/calculator/?from=GBP&to=SEK&amount=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    rate_text = soup.find("span", class_="ccOutputRslt").text

    clean = re.sub(r"[^\d.]", "", rate_text)

    return float(clean)


def convert_to_sek(price_text, rate):
    clean = re.sub(r"[^\d.]", "", price_text)
    gbp = float(clean)

    sek = gbp * rate

    return round(sek, 2)


# HÄMTA BÖCKER FRÅN KATEGORI

def get_books_from_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, "lxml")

    books = []
    articles = soup.find_all("article", class_="product_pod")

    rate = get_exchange_rate()

    for book in articles:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]

        # 🔥 RENSAR priset med regex (tar bort Â£ etc.)
        clean_price = re.sub(r"[^\d.]", "", price)

        books.append({
            "id": len(books) + 1,
            "title": title,
            "price_gbp": clean_price,   # ← sparar rensat pris
            "price_sek": convert_to_sek(price, rate),
            "rating": rating
        })

    return books


# SPARA BÖCKER MED DATUM

def save_books(category_name, category_url):
    today = datetime.now().strftime("%y%m%d")
    filename = f"data/{category_name}_{today}.json"

    os.makedirs("data", exist_ok=True)

    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)

    books = get_books_from_category(category_url)

    with open(filename, "w") as f:
        json.dump(books, f, indent=4)

    return books


# CRUD

def load_books_file(category_name):
    today = datetime.now().strftime("%y%m%d")
    filename = f"data/{category_name}_{today}.json"

    os.makedirs("data", exist_ok=True)

    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f), filename

    return [], filename


def add_book(category_name, new_book):
    if not new_book or "title" not in new_book:
        return {"error": "Invalid data"}

    books, filename = load_books_file(category_name)

    new_book["id"] = len(books) + 1
    books.append(new_book)

    with open(filename, "w") as f:
        json.dump(books, f, indent=4)

    return new_book


def update_book(category_name, book_id, updated_data):
    books, filename = load_books_file(category_name)

    for book in books:
        if book["id"] == book_id:
            book.update(updated_data)

            with open(filename, "w") as f:
                json.dump(books, f, indent=4)

            return book

    return {"error": "Book not found"}


def delete_book(category_name, book_id):
    books, filename = load_books_file(category_name)

    new_books = [b for b in books if b["id"] != book_id]

    if len(new_books) == len(books):
        return {"error": "Book not found"}

    with open(filename, "w") as f:
        json.dump(new_books, f, indent=4)

    return {"message": "Book deleted successfully"}