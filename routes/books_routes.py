from flask import Blueprint, jsonify, request
from services.scraper import (
    save_categories,
    load_categories_from_file,
    save_books,
    add_book,
    update_book,
    delete_book
)

# Skapar en Blueprint för alla bok-relaterade routes
books_bp = Blueprint("books", __name__)


# HOME — test om API fungerar
@books_bp.route("/")
def home():
    return "Webscraping API fungerar!"


# KATEGORIER

# Hämtar alla kategorier
@books_bp.route("/api/v1/categories", methods=["GET"])
def categories():
    # Läser från fil eller skapar fil om den saknas
    return jsonify(load_categories_from_file())


# BÖCKER - GET ALLA

# Hämtar alla böcker i en kategori
@books_bp.route("/api/v1/books/<category_name>", methods=["GET"])
def books(category_name):

    categories = load_categories_from_file()

    category_url = None
    # Letar efter rätt kategori
    for cat in categories:
        if cat["name"].lower() == category_name.lower():
            category_url = cat["url"]
            break

    if not category_url:
        return jsonify({"error": "Category not found"}), 404

    return jsonify(save_books(category_name, category_url))


# BÖCKER - GET EN BOK

# Hämtar en specifik bok via ID
@books_bp.route("/api/v1/books/<category_name>/<int:book_id>", methods=["GET"])
def get_single_book(category_name, book_id):

    categories = load_categories_from_file()

    category_url = None
    for cat in categories:
        if cat["name"].lower() == category_name.lower():
            category_url = cat["url"]
            break

    if not category_url:
        return jsonify({"error": "Category not found"}), 404

    books = save_books(category_name, category_url)

    for book in books:
        if book["id"] == book_id:
            return jsonify(book)

    return jsonify({"error": "Book not found"}), 404


# POST - Lägg till bok

# Lägger till ny bok i filen
@books_bp.route("/api/v1/books/<category_name>", methods=["POST"])
def add_new_book(category_name):
    data = request.json
    return jsonify(add_book(category_name, data))


# PUT - Uppdatera bok

# Uppdaterar befintlig bok
@books_bp.route("/api/v1/books/<category_name>/<int:book_id>", methods=["PUT"])
def update_existing_book(category_name, book_id):
    data = request.json
    return jsonify(update_book(category_name, book_id, data))


# DELETE - Ta bort bok

# Tar bort bok via ID
@books_bp.route("/api/v1/books/<category_name>/<int:book_id>", methods=["DELETE"])
def delete_existing_book(category_name, book_id):
    return jsonify(delete_book(category_name, book_id))