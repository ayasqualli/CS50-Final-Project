import requests
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required


# Initialize Flask application
app = Flask(__name__)

# Configure SQLAlchemy for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_recommendation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define database models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    authors = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    thumbnail = db.Column(db.String, nullable=True)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Google Books API URL
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# Helper function to fetch books from Google Books API
def fetch_books(query):
    params = {
        "q": query,
        "key": 'AIzaSyCBMMMwbqwKEypOr3XOM_Tg29p3dnFmS7Q',  # Replace with your actual Google API key
        'maxResults': 10
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return []

# Home route
@app.route("/")
@app.route("/home")
def home():
    if "user_id" in session:
        user = Users.query.filter_by(id=session["user_id"]).first()
        favorite_books = user.favorites
        return render_template("home.html", favorite_books=favorite_books)
    else:
        return render_template("home.html")

# Search route
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        books = fetch_books(query)
        return render_template("search_results.html", books=books)
    return render_template("search.html")

# Book detail route
@app.route("/book/<book_id>")
def book_detail(book_id):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes/{book_id}")
    book = response.json()
    return render_template("book_detail.html", book=book)

# Search profile route
@app.route("/search_profile", methods=["POST"])
@login_required
def search_profile():
    data = request.get_json()
    query = data.get('query', '')
    books = fetch_books(query)
    return jsonify({"items": books})

# Add favorite route
@app.route("/favorite/<book_id>", methods=["POST"])
@login_required
def add_favorite(book_id):
    if "user_id" not in session:
        flash("Please log in to add books to your favorites.", "error")
        return redirect(url_for("login"))

    response = requests.get(f"https://www.googleapis.com/books/v1/volumes/{book_id}")
    book = response.json()

    user_id = session.get("user_id")
    title = book['volumeInfo'].get('title')
    authors = ", ".join(book['volumeInfo'].get('authors', []))
    description = book['volumeInfo'].get('description')
    thumbnail = book['volumeInfo'].get('imageLinks', {}).get('thumbnail')

    new_favorite = Favorites(user_id=user_id, book_id=book_id, title=title, authors=authors, description=description, thumbnail=thumbnail)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Book added to favorites."})

# Profile route
@app.route("/profile")
@login_required
def profile():
    user_id = session.get("user_id")
    user = Users.query.filter_by(id=user_id).first()
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return render_template("profile.html", username=user.username, favorites=favorites)

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")

        if not name or not password:
            flash("You must provide a username and a password")
            return render_template("login.html")

        user = Users.query.filter_by(username=name).first()
        if user is None or not check_password_hash(user.password, password):
            flash("Invalid username and/or password")
            return render_template("login.html")

        session["user_id"] = user.id
        return redirect(url_for("profile"))
    else:
        return render_template("login.html")

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")

        if not name:
            flash("You must provide a valid username")
            return render_template("register.html")

        elif not password:
            flash("You must provide a valid password")
            return render_template("register.html")

        elif password != request.form.get("confirmation"):
            flash("Passwords must match")
            return render_template("register.html")

        user = Users.query.filter_by(username=name).first()
        if user is not None:
            flash("Username already exists")
            return render_template("register.html")

        password = generate_password_hash(password)
        new_user = Users(username=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        user = Users.query.filter_by(username=name).first()
        session["user_id"] = user.id
        return redirect(url_for("login"))
    else:
        return render_template("register.html")

# Logout route
@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect(url_for('home'))

# Remove favorite route
@app.route("/remove_favorite/<int:favorite_id>", methods=["DELETE"])
@login_required
def remove_favorite(favorite_id):
    favorite = Favorites.query.get(favorite_id)
    if favorite and favorite.user_id == session["user_id"]:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite removed successfully"}), 200
    return jsonify({"message": "Favorite not found or not authorized"}), 404

# Main block to run the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
