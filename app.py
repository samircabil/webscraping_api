from flask import Flask
from routes.books_routes import books_bp

# Skapar själva Flask-applikationen
app = Flask(__name__)

# Registrerar blueprinten som innehåller alla routes för böcker
app.register_blueprint(books_bp)

# Kör appen lokalt om filen startas direkt (inte via server)
if __name__ == "__main__":
    app.run(debug=True)