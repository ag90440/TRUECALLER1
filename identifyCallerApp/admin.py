from django.contrib import admin
from .models import AppUser, PhoneNumber, SpamReport, UserContact


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone_number", "is_superuser"]
    search_fields = ["name", "phone_number", "email"]
    list_filter = ["is_superuser", "is_active"]
    ordering = ["name"]


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ["name", "number", "spam_likelihood"]
    search_fields = ["name", "number"]
    list_filter = ["spam_likelihood"]
    ordering = ["number"]


@admin.register(UserContact)
class UserContactAdmin(admin.ModelAdmin):
    list_display = ["user", "contact_name", "contact_number"]
    search_fields = ["contact_name", "contact_number"]
    ordering = ["contact_name"]


@admin.register(SpamReport)
class SpamReportAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "marked_as_spam"]
    list_filter = ["marked_as_spam"]
    ordering = ["phone_number"]
