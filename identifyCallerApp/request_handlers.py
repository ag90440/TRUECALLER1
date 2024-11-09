from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import AppUser, PhoneNumber, SpamReport, UserContact
from django.contrib import messages
from django.urls import reverse


def index(request):
    """Display the main page if the user is authenticated; otherwise, redirect to login."""
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'identifyCallerApp/index.html')


def sign_up_user(request):
    """Handle user registration with name, phone number, and optional email."""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if AppUser.objects.filter(phone_number=phone).exists():
            context = {"msg": "A user with this phone number already exists. Please use a different number."}
            return render(request, 'identifyCallerApp/signup.html', context)

        user = AppUser.objects.create_user(name=name, phone_number=phone, email=email, password=password)
        messages.success(request, 'Account created successfully. Please log in.')
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'identifyCallerApp/signup.html')


def login_user(request):
    """Authenticate and log in the user."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            context = {"message": "Invalid credentials. Please try again."}
            return render(request, 'identifyCallerApp/login.html', context)

    return render(request, 'identifyCallerApp/login.html')


def logout_user(request):
    """Log out the user and redirect to login page."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return HttpResponseRedirect(reverse('login'))


def mark_as_spam(request, query):
    """Mark a phone number as spam and update its spam likelihood."""
    if not request.user.is_authenticated:
        return redirect('/login')

    user = request.user
    phone_instance, created = PhoneNumber.objects.get_or_create(number=query)

    spam_report, created = SpamReport.objects.get_or_create(user=user, phone_number=phone_instance)
    if not spam_report.marked_as_spam:
        spam_report.marked_as_spam = True
        spam_report.save()
        phone_instance.spam_likelihood += 1
        phone_instance.save()

    return JsonResponse({"message": "Phone number has been marked as spam."})


def search_person_by_name(request, query):
    """Search for contacts by name, returning both exact and partial matches."""
    starts_with_results = PhoneNumber.objects.filter(name__startswith=query).values()
    contains_results = PhoneNumber.objects.filter(name__icontains=query).exclude(name__istartswith=query).values()

    results = list(starts_with_results) + list(contains_results)
    search_results = [
        {"name": res['name'], "phone_number": res['number'], "spam_likelihood": res['spam_likelihood']}
        for res in results
    ]

    return JsonResponse({'results': search_results})


def search_person_by_number(request, query):
    """Search for a contact by phone number, returning results with spam likelihood."""
    if not query.isdigit() or len(query) < 10:
        return JsonResponse({'error': 'Invalid phone number format'}, status=400)

    try:
        registered_user = AppUser.objects.get(phone_number=query)
        is_contact = UserContact.objects.filter(user=registered_user, phone_number=request.user.phone_number).exists()
        most_spammed = PhoneNumber.objects.filter(number=query).order_by('-spam_likelihood').first()

        result_info = {
            'name': registered_user.name,
            'phone_number': registered_user.phone_number,
            'email': registered_user.email if is_contact else None,
            'spam_likelihood': most_spammed.spam_likelihood if most_spammed else 0
        }

        return JsonResponse({'result': result_info})

    except AppUser.DoesNotExist:
        phone_entries = PhoneNumber.objects.filter(number=query)
        search_results = [
            {"name": entry.name, "phone_number": entry.number, "spam_likelihood": entry.spam_likelihood}
            for entry in phone_entries
        ]
        return JsonResponse({'results': search_results})

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
