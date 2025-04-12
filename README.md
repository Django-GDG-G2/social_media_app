# Social Media App

Welcome to the Social Media App! This is a powerful, scalable, and secure web-based application designed to offer a seamless social experience with a RESTful API backend. This project enables mobile and web applications to interact with the app’s services through clean and efficient API endpoints.

---

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [Technologies Used](#technologies-used)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Project Description

The **Django Social Media App** is a dynamic social platform built with Django and Django Rest Framework. It supports user authentication, profile management, post creation, comments, likes, and follow/unfollow functionality. The backend exposes a RESTful API that can be consumed by both web and mobile applications.

---

## Features

- **User Authentication**: Register, log in, and log out using JWT tokens.
- **User Profiles**: Users can create, edit, and view profiles, including bios and personal details.
- **Posts**: Create, edit, and delete posts. Users can add text and images to their posts.
- **Interactions**: Like/unlike posts and comment on them.
- **Follow System**: Follow/unfollow users and view a list of followers and followings.

---

## Installation

To run the project locally, follow these steps:

### Prerequisites

- Python 3.x
- Django
- Django REST Framework
- SQLite (initial database)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/social-media-app.git
   cd social-media-app
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations to set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

Now, your app should be running at `http://127.0.0.1:8000/`.

---

## Technologies Used

- **Django**: The backend framework for building the application.
- **Django REST Framework**: Used for building the API.
- **JWT Authentication**: For secure user login/logout.
- **SQLite**: For the initial database setup.

---

## API Endpoints

### Authentication Endpoints

- **POST** `/api/auth/register`: Register a new user
- **POST** `/api/auth/login`: Login and get JWT token
- **POST** `/api/auth/logout`: Log out (invalidate JWT token)

### User Profile Endpoints

- **GET** `/api/users/{user_id}`: Retrieve a user's profile
- **PUT** `/api/users/{user_id}`: Update a user's profile

### Post Endpoints

- **POST** `/api/posts`: Create a new post
- **GET** `/api/posts/{post_id}`: Retrieve a specific post
- **PUT** `/api/posts/{post_id}`: Edit a post
- **DELETE** `/api/posts/{post_id}`: Delete a post

### Interaction Endpoints

- **POST** `/api/posts/{post_id}/like`: Like a post
- **POST** `/api/posts/{post_id}/comment`: Comment on a post

### Follow System Endpoints

- **POST** `/api/users/{user_id}/follow`: Follow a user
- **POST** `/api/users/{user_id}/unfollow`: Unfollow a user

---
🖥️ TemplateView Accessibility
The TemplateViews provide a user-friendly HTML interface for interacting with the app directly in a web browser. These pages are accessible without needing external tools like Postman. For example:

Go to /register/ to sign up

Visit /login/ to log in

Browse /posts/ to view all posts

Access /users/ to explore user profiles

In addition to the RESTful API, the app includes basic TemplateViews that serve HTML pages. These templates are a work-in-progress and are currently designed to mock a simplified version of Instagram (inspired by "DjangoGram").

They provide a visual way to:

Register and log in

View and create posts

Browse users and profiles

Follow/unfollow users

Like and comment on posts

🔧 Planned Improvements:

The current templates are placeholders and will be revamped with improved UI/UX.

Features like real-time likes and comments, and enhanced interactivity will be re-implemented with better front-end logic (potentially using JavaScript or React).

## Data Models

### User Model
- **id**: Integer (Auto-incremented)
- **email**: String (Unique)
- **username**: String (Unique)
- **password**: String (Hashed)
- **bio**: Text (Optional)
- **is_active**: Boolean (Default: True)
- **date_joined**: DateTime (Automatically set)

### Post Model
- **id**: Integer (Auto-incremented)
- **user**: ForeignKey (User)
- **content**: Text
- **created_at**: DateTime (Automatically set)
- **updated_at**: DateTime (Automatically set)

### Comment Model
- **id**: Integer (Auto-incremented)
- **user**: ForeignKey (User)
- **post**: ForeignKey (Post)
- **content**: Text
- **created_at**: DateTime (Automatically set)

### Like Model
- **id**: Integer (Auto-incremented)
- **user**: ForeignKey (User)
- **post**: ForeignKey (Post)
- **created_at**: DateTime (Automatically set)

### Follow Model
- **id**: Integer (Auto-incremented)
- **follower**: ForeignKey (User)
- **following**: ForeignKey (User)
- **created_at**: DateTime (Automatically set)

---

## Usage

Once the app is up and running, you can test the API via tools like **Postman** or **Swagger**. All endpoints are ready to be consumed by front-end or mobile applications. You can also interact with the admin panel using the superuser account.

---


### Generally

This project is designed to scale, handle increasing activity efficiently, and provide a secure user experience. The JWT-based authentication system ensures secure logins and logout functionality. The use of Django REST Framework ensures the API is clean, simple, and highly extensible.

---

