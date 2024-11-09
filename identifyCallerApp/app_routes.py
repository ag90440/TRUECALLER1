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
