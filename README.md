
# 📚 BookWise: Discover Your Next Great Read  

## 🌟 Uncover Hidden Gems and Dive into Literary Adventures

### Video Demo

                                   https://youtu.be/JQICy_JFegM

### Description

BookWise is more than just a search engine; it’s your literary companion. With seamless integration of the Google Books API, we empower you to:

*Search with Precision* : Find books by title, author, or reference. Our intelligent search engine delivers accurate results, so you can dive into the perfect read.

*Explore Rich Metadata*: Discover not only the book’s title and author but also a captivating brief about its essence. Uncover hidden gems waiting to be explored.

*Personalize Your Library*: Sign up to unlock your profile page. Easily manage your favorite books—add new finds, remove old ones, and curate your literary collection.

BookWise: Where words come alive. Start your reading journey today! 🌟

## How to Run

> **Installation**

1. Clone the repository:

```sh
git clone https://github.com/ayasqualli/CS50-Final-Project.git
```

2. Navigate to the project directory

```sh
cd BookWise
```

3. Create a virtual envorinment(optional but recommended)

```sh
python -m venv venv
source venv/bin/activate   # On Windows use 'ven\Scripts\activate
```

4. Install dependecies

```sh
pip install -r requirements.txt
```

5. Set up the database

```sh
flask db init
flask db migrate
flask db upgarde
```

6. Run the application

```sh
flask run
```

7. Access the application
Open your browser and go to `localhost:5000/`

## app.py

First things first. This file is the backbone of all this project.  
After importing all the necessary libraries ( requests, flask, flask_session, flask_sqlalchemy,tempfile, werkzeug.security) we can start configuring the app, as for the database, it is powered by **SQLAlchemy**.

### Features

>*User Authentication*:

Users can register, log in, and log out.
Passwords are securely hashed using werkzeug.security.

> *Database Models*:

The application uses SQLAlchemy to define two database models:

- Users: Stores user information (username, password, favorites).
- Favorites: Stores favorite books associated with users.  

>*Routes and Views*:

- `/home`: Displays favorite books (if logged in) or the home page.
- `/search`: Allows users to search for books.
- `/book/<book_id>`: Displays details of a specific book.
- `/profile`: Shows user profile and favorite books.

>*Google Books API Integration*:

The application fetches book data from the Google Books API.
Users can search for books and view details.

>*Session Management*:

Flask sessions handle user authentication.

## helpers.py

This file is used to define the method **@login_required**

>*Import Statements*:

The snippet begins with import statements for necessary modules:  
`from flask import redirect, session`  
This imports the redirect function and the session object from the Flask framework. These are used for handling HTTP redirects and managing user sessions, respectively.

>*Decorator Definition*:

The `login_required` decorator is defined. Decorators in Python are functions that modify or enhance other functions.
It takes a single argument, `f`, which represents the function being wrapped (the view function that requires login).
The `@wraps(f)` line ensures that the decorated function retains its original name and docstring.

>*Wrapper Function*:

Inside the `login_required` decorator, there’s a nested function called `wrap`.
This wrapper function is what gets executed when the decorated route is accessed.
It checks whether the user is logged in by examining the session object.
If the user is logged in (i.e., the `"user_id"` key exists in the session), the original view function `(f(*args, **kwargs))` is called.
If the user is not logged in, a flash message is displayed (indicating the need to log in) and the user is redirected to the `/welcome` page.

## Home Page

This HTML template is designed for the home page. It includes a header with the site title, a main content area with a search form, and conditional links for user actions based on authentication status. The footer includes a copyright notice. The template uses Jinja2 for dynamic content generation, making it adaptable to different user states and actions. The linked CSS file (styles.css) is used to style the page.  

- `<meta charset="UTF-8">`:Specifies the character encoding for the document, which is UTF-8.
- `<title>Home</title>`: Sets the title of the web page, which appears in the browser tab.
- `<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">`:
Links an external CSS file (styles.css) for styling the web page. The {{ url_for('static', filename='styles.css') }} is a Jinja2 template syntax used to dynamically generate the correct URL for the static file.
- `<body>`: Contains the content of the HTML document.
- `<header>`: Encloses the introductory content or navigational links.In this case it only have the header
`<h1>` that displays the header "Welcome to BookWise".
- `<main>`: Specifies the main content of the document.
- `<form>`: Defines an HTML form used to collect user input.
- `action="{{ url_for('search') }}"`: This action dynamically specifies the URL to which the form will be submitted upon using Jinja2
- `method="post"`: Indicates the form submission method is POST.
- `class="search"`: Assigns a class name for styling purposes.
- `<input type="text" name="query" placeholder="Search for books">`: An input field for the search query.
- `<button type="submit">Search</button>`: A submit button for the form.
- `<br>`: Adds a line break.

>Conditional Content Display:

- `{% if user_id %} ... {% else %} ... {% endif %}`: Jinja2 conditional statement to display different links based on user authentication status.

- *Authenticated User Links*:

  - `<a href="{{ url_for('profile') }}">Go to profile</a>`: Link to the user's profile.
  - `<a href="{{ url_for('logout') }}">Logout</a>`: Link to log out.

- *Unauthenticated User Links*:
  - `<a href="{{ url_for('login') }}">Login</a>`: Link to the login page.
  - `<a href="{{ url_for('register') }}">Register</a>`: Link to the registration page.

As for the footer i've chosen a simple footer conataing just the year of production of this project as well as a little copyright tag :  

```html
    <footer>
        <p>&copy; 2024 Book Recommendation</p>
    </footer>
```

> [!IMPORTANT]  
> The first 7- line of code are almost the same for all the HTML templates as well as the footer (just the title changing) so no need to explain them again. For further info, you can refer to the prevoius section

## Login Page

This HTML template creates the login page. It includes a header with the page title, a main section with a login form, and links for user registration and navigating back to the home page. The footer includes a copyright notice. The template uses Jinja2 for dynamic URL generation and incorporates basic form elements with required fields.

> *Login Form*:

- `<form class="login-form" action="{{ url_for('login') }}" method="post">`: Defines the login form. The action attribute points to the URL for form submission, dynamically generated using Jinja2. The method attribute specifies POST for form submission.

- `<h2>Login</h2>`: A subheading for the form.

> *Username Field*:

- `<label for="username">Username</label>`: Label for the username input field.
- `<input type="text" id="username" name="username" placeholder="Username" required>`: Input field for the username, with a placeholder and the required attribute to ensure it is filled out.

> *Password Field*:

- `<label for="password">Password</label>`: Label for the password input field.
- `<input type="password" id="password" name="password" placeholder="Password" required>`: Input field for the password, with a placeholder and the required attribute.
- `<button type="submit">Login</button>`: Submit button for the form.

> *Additional Links*:

- `<div class="centered-links">`: Div container for centered links.
- `<a href="{{ url_for('register') }}">Don't have an account? Register here.</a>`: Link to the registration page.
- `<a href="{{ url_for('home') }}">Back to Home</a>`: Link to the home page.

## Registration Page

This HTML template creates the registration page. It includes a header with the page title, a main section with a registration form, and links for user login and navigating back to the home page. The footer includes a copyright notice. The template uses Jinja2 for dynamic URL generation and incorporates basic form elements with required fields, including an error message placeholder.

>*Registration Form*:

- `<form class="registration-form" action="{{ url_for('register') }}" method="post">`: Defines the registration form. The action attribute points to the URL for form submission, dynamically generated using Jinja2. The method attribute specifies POST for form submission.

- `<h2>Register</h2>`: A subheading for the form.

>*Username Field*:

- `<label for="username">Username:</label>`: Label for the username input field.
- `<input type="text" name="username" id="username" placeholder="Username" required>` : Input field for the username, with a placeholder and the required attribute to ensure it is filled out.

>*Password Field*:

- `<label for="password">Password</label>`: Label for the password input field.
- `<input type="password" id="password" name="password" placeholder="Password" required>`: Input field for the password, with a placeholder and the required attribute.

>*Confirm Password Field*:

- `<label for="confirmation">Confirm Password</label>`: Label for the password confirmation input field.
-`<input type="password" id="confirmation" name="confirmation" placeholder="Confirm Password" required>`: Input field for confirming the password, with a placeholder and the required attribute.

>*Error Message*:

- `<div class="error-message">`: Div container for displaying error messages.
- `{{ error_message }}`: Jinja2 template syntax to display any error messages.
- `<button type="submit">Register</button>`: Submit button for the form.

>*Additional Links*:

- `<div class="centered-links">`: Div container for centered links.
- `<a href="{{ url_for('login') }}">Already have an account? Login here.</a>`: Link to the login page.
- `<a href="{{ url_for('home') }}">Back to Home</a>`: Link to the home page.

## base.html

This HTML template is the base for the pages that are going to use employing the Jinja2 framework.
It includes a header with a navigation bar that changes based on the user's login status, a main content section with a placeholder for dynamic content, and a footer with a copyright notice. The template uses Jinja2 for dynamic URL generation and session handling.

- `<header>` : Encloses the navigational links and the title bar.
- `<h1>BookWise</h1>`: Displays the main heading "BookWise".
- `<nav>`: Navigation bar that changes based on the user's login status:
- `{% if session.logged_in %}`: Checks if the user is logged in.
  - `<p>Welcome, {{ session.username }}!`: Displays a welcome message with the user's username.
  - `<a href="{{ url_for('profile') }}">Profile</a>`: Link to the user's profile.
  - `<a href="{{ url_for('logout') }}">Logout</a>`: Link to log out.
- `{% else %}`: If the user is not logged in:
  - `<a href="{{ url_for('login') }}">Login</a>`: Link to the login page.
  - `<a href="{{ url_for('register') }}">Register</a>`: Link to the registration page.
- `<main>`: Contains the main content of the page.
- `{% block content %}{% endblock %}`: Placeholder for content that will be inserted by other templates extending this base template.

## Search Results Page

This Jinja2 template extends the base template and provides a structured layout for displaying search results. It includes dynamic content for listing book details and a script for adding books to favorites via an AJAX request. The template uses Jinja2 for looping through book data and rendering HTML elements with data attributes for use in JavaScript.

- `{% extends "base.html" %}`: Extends the base template to create the serach results' one.
- `{% block content %}...{% endblock %}`: This block defines the content to be inserted into block content section of the base template.4

>*Search Result Section*

- `<div class="search-results">`: Div container for the search results.
-`<h2>Results for your query</h2>`: Heading for the search results section.
-`<ul>`: Unordered list to contain the search results.
  - `{% for book in books %}`: Loop through each book in the books list.
  - `<li class="book-item">`: List item for each book with a class of book-item.
  - `<h3>{{ book.volumeInfo.title }}</h3>`: Displays the book title.
  - `<p><strong>Authors:</strong> {{ book.volumeInfo.authors | join(', ') }}</p>`: Displays the authors, joined by commas.
  - `<p><strong>Published Date:</strong> {{ book.volumeInfo.publishedDate }}</p>`: Displays the published date.
  - `<p>{{ book.volumeInfo.description }}</p>`: Displays the book description.
  - **Favorite Button**:
    - `<button class="favorite-btn" data-book-id="{{ book.id }}"`: Button to add the book to favorites. It includes data attributes for the book details.
- `<a href="{{ url_for('home') }}">Back to Home</a>`: Link to navigate back to the home page.

>*JavaScript for Adding Favourites*

- **Script Tag**: Contains JavaScript to handle adding books to favorites.
- **Event Listener**:
  - `document.querySelectorAll('.favorite-btn').forEach(button => { ... })`: Selects all elements with the class `favorite-btn` and adds a click event listener to each button.
  - `const bookId = button.getAttribute('data-book-id');`: Retrieves the book ID from the data attribute.
  - `fetch('/add_favorite', { ... })`: Sends a POST request to the /add_favorite endpoint with the book details in the request body.
  - `button.disabled = true;`: Disables the button after it is clicked to prevent multiple submissions.

## Profile Page

This Jinja2 template generates a user profile page for the "BookWise" website. It displays the user's favorite books and provides functionality to remove books from favorites and search for new books. The template includes dynamic content rendering, form handling, and AJAX requests to manage favorites without reloading the page

>*Profile Section*

- `<div class="profile">`: Div container for the profile section.
- `<h2>{{ username }}'s Profile</h2>`: Displays the username's profile title dynamically.
- **Favorite Books List**:
  - `<h3>Your Favorite Books</h3>`: Subheading for the favorite books section.
  - `{% for favorite in favorites %}`: Loops through each favorite book.
    - `<li class="favorite-book">`: List item for each favorite book.
    - `<h4>{{ favorite.title }}</h4>`: Displays the book title.
    - `<p><strong>Authors:</strong> {{ favorite.authors }}</p>`: Displays the authors.
    - `<p><strong>Published Date:</strong> {{ favorite.published_date }}</p>`: Displays the published date.
    - `<p>{{ favorite.description }}</p>`: Displays the book description.
    - **Remove Button**:
      - `<button class="remove-favorite-btn" data-favorite-id="{{ favorite.id }}">Remove from Favorites</button>`: Button to remove the book from favorites.

>*Search Section*

- `<div class="search">`: Div container for the search form.
- **Search Form**:
  - `<form action="{{ url_for('search_profile') }}" method="post">`: Form to submit search queries.
  - `<input type="text" name="query" placeholder="Search for books">`: Input field for the search query.
  - `<button type="submit">Search</button>`: Button to submit the search form.

- `<div id="search-results">`: Div container where search results will be displayed.

>*Navigation Links*

- `<div class="centered-links">`: Div container for navigation links.
- **Home and Logout Links**:
  - `<a href="{{ url_for('home') }}">Home</a>`: Link to the home page.
  - `<a href="{{ url_for('logout') }}">Logout</a>`: Link to log out.

>*JavaScript Section*

- ***Favorite Button***:
  - **Event Listener**:
    - `document.querySelectorAll('.remove-favorite-btn').forEach(button => { ... })`: Selects all elements with the class remove-favorite-btn and adds a click event listener to each button.
    - `fetch(/remove_favorite/${favoriteId}, { method: 'DELETE' })`: Sends a DELETE request to remove the book from favorites.
    - `button.closest('li').remove();`: Removes the book item from the DOM after successful deletion.
- ***Search Form Submission***:
  - **Event Listener**:
  - `document.querySelector('.search form').addEventListener('submit', function(event) { ... })`: Adds a submit event listener to the search form.
  - `fetch(/search_profile, { method: 'POST', body: JSON.stringify({ query: query }), headers: { 'Content-Type': 'application/json' } })`: Sends a POST request to search for books.
  - `resultsContainer.innerHTML = '';`: Clears previous search results.
  - `data.items.forEach(item => { ... })`: Loops through search results and appends them to the results container.
  - *Add Favorite Button*:
    - `fetch(/favorite/${bookId}, { method: 'POST' })`: Sends a POST request to add the book to favorites.

## CSS Formatting

The CSS file provide the foundational styling for the web application's layout, including the body, header, forms, buttons, search results, profile, and footer sections.

Here are the most important sections of code that provide a consistent and clean apprearance for all the website:

> *General Styling*

```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    align-items: center;
    justify-content: center;
    padding: 0;
    background-color: #f4f4f4;
    color: #333;
}
```

> *Header and Navigation*

```css
header {
    background-color: #c5a3ff;
    color: white;
    padding: 10px 0;
    text-align: center;
}

nav a {
    color: white;
    margin: 0 10px;
    text-decoration: none;
}
```

> *Forms*

```css
.login-form, .registration-form {
    max-width: 400px;
    margin: 0 auto;
    background-color: white;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login-form button, .registration-form button {
    width: 100%;
    padding: 10px;
    background-color: #c5a3ff;
    color: white;
    border: none;
    cursor: pointer;
}
```

> *Search Section*

```css
.search input[type="text"] {
    padding: 10px;
    width: 300px;
}

.search button {
    padding: 10px;
    background-color: #c5a3ff;
    color: white;
    border: none;
    cursor: pointer;
}
```

> *Search Results*

```css
.search-results .book-item {
    background-color: white;
    margin: 10px 0;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.favorite-btn, .remove-favorite-btn {
    padding: 10px;
    background-color: #c5a3ff;
    color: white;
    border: none;
    cursor: pointer;
    margin-top: 10px;
}
```

> *Profile Section*

```css
.profile {
    max-width: 600px;
    margin: 0 auto;
    background-color: white;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.profile .favorite-book {
    background-color: white;
    margin: 10px 0;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    text-align: left;
}
```

> *Footer*

```css
footer {
    text-align: center;
    padding: 10px 0;
    background-color: #f4f4f4;
    color: #333;
}
```

___
***All credits go to CS50 : Introduction to Computer Science, and i thank my univerty teachers at @UM6P, and also credits for the help i got from ChatGPT especially with the CSS and also for debbuging help from @Agathasta***
