# Truecaller-like Application

This is a Django-based application designed to simulate some functionalities of Truecaller, such as user registration, login, and the ability to mark phone numbers as spam or search for users by name or number.

## Features

- User Registration, Login, and Logout
- Mark phone numbers as spam
- Search for users by name or phone number
- Basic administrative functionalities


## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/TRUECALLER1.git
    cd TRUECALLER1
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser** (for accessing the admin panel):
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the Application**:
    - Open your browser and go to `http://127.0.0.1:8000` to view the application.

## Routes

Below are the main routes defined in the application:

```python
from django.urls import path
from . import request_handlers

urlpatterns = [
    path('', request_handlers.index, name="index"),                           # Home page route
    path('login/', request_handlers.login_user, name="login"),                # User login route
    path('logout/', request_handlers.logout_user, name="logout"),             # User logout route
    path('signup/', request_handlers.sign_up_user, name="signup"),            # User signup route
    path('markSpam/<str:query>/', request_handlers.mark_as_spam, name="mark_as_spam"),  # Mark a phone number as spam
    path('search/name/<str:query>/', request_handlers.search_person_by_name, name="search_by_name"),  # Search by name
    path('search/number/<str:query>/', request_handlers.search_person_by_number, name="search_by_number"),  # Search by number
]
