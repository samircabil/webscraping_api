from flask import Blueprint, jsonify, request
from services.scraper import (
    save_categories,
    load_categories_from_file,
    save_books,
    add_book,
    update_book,
    delete_book
)

books_bp = Blueprint("books", __name__)


# HOME
@books_bp.route("/")
def home():
    return "Webscraping API fungerar!"


# KATEGORIER

@books_bp.route("/api/v1/categories", methods=["GET"])
def categories():
    # Sparar om filen EN gång om den inte finns
    return jsonify(load_categories_from_file())


# BÖCKER - GET ALLA

@books_bp.route("/api/v1/books/<category_name>", methods=["GET"])
def books(category_name):

    categories = load_categories_from_file()

    category_url = None
    for cat in categories:
        if cat["name"].lower() == category_name.lower():
            category_url = cat["url"]
            break

    if not category_url:
        return jsonify({"error": "Category not found"}), 404

    return jsonify(save_books(category_name, category_url))


# BÖCKER - GET EN BOK


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

@books_bp.route("/api/v1/books/<category_name>", methods=["POST"])
def add_new_book(category_name):
    data = request.json
    return jsonify(add_book(category_name, data))


# PUT - Uppdatera bok

@books_bp.route("/api/v1/books/<category_name>/<int:book_id>", methods=["PUT"])
def update_existing_book(category_name, book_id):
    data = request.json
    return jsonify(update_book(category_name, book_id, data))


# DELETE - Ta bort bok

@books_bp.route("/api/v1/books/<category_name>/<int:book_id>", methods=["DELETE"])
def delete_existing_book(category_name, book_id):
    return jsonify(delete_book(category_name, book_id))