# BookManagementSystem

## Introduction

BookManagementSystem is a Flask-based web application designed to manage books, user accounts, and interactions such as wishlist and liked books.

## Features

- **User Management:**
  - User registration with username, email, and password.
  - User login and logout with JWT authentication.
  - User profile management (update and delete).
  - User roles and permissions.

- **Book Management:**
  - Add new books with details like title, author, ISBN, published date, pages, cover image, and language.
  - Update and delete existing books.
  - View a list of all books.

- **User Interactions:**
  - Add books to a wishlist.
  - Like books and keep track of liked items.

- **Security:**
  - Token-based authentication using JWT (JSON Web Tokens).
  - Token revocation and blacklisting for secure logout.

- **Data Validation:**
  - Utilizes Pydantic for robust data validation across API endpoints.

- **Middleware:**
  - Custom middleware ensures secure handling of request and response bodies, including validation against defined Pydantic models.


## Installation

1. Clone the repository:

   ```bash
    git clone <repository_url>
    cd BookManagementSystem

2. Create and activate a virtual environment:

   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:

   ```bash
    pip install -r requirements.txt

4. Set up the database:

   ```bash
    flask db init
    flask db migrate
    flask db upgrade

5. Run the application:

   ```bash
   flask run

### The application should now be running at http://localhost:5000.


## API Documentation
***The API documentation is available through Swagger UI, powered by Flask-RESTx.***

/user/register: Register a new user.
/user/login: Login with email and password.
/user/logout: Logout and revoke tokens.
/user/me: Retrieve and update user profile.


- **Auth API:**
  - /user/login: Login with email and password.
  - /user/logout: Logout and revoke tokens. 
  - /user/refresh: refresh access tokens.

- **User API:**
  - /user/register: Register a new user.
  - /user/me: Retrieve, update and delete user profile.

- **Book API:**
  - /books/: Get a list of all books and create book.
  - /books/<id>: Get, update, or delete a specific book.
  - /books/liked: Manage liked books.
  - /books/wishlist: Manage books in the wishlist.
