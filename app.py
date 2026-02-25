from flask import Flask
from routes.books_routes import books_bp

app = Flask(__name__)

app.register_blueprint(books_bp)

if __name__ == "__main__":
    app.run(debug=True)