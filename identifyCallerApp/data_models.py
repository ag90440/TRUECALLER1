from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.db import models


class AppUserManager(BaseUserManager):
    """Manager for creating regular and superuser accounts."""

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError("An email or phone number is required")
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    """User model that supports authentication using a phone number."""

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AppUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'name']

    groups = models.ManyToManyField(Group, related_name='appuser_groups', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='appuser_permissions',
        blank=True,
        help_text='Permissions for this user.',
        verbose_name='User Permissions',
    )

    def __str__(self):
        return self.phone_number or self.email


class PhoneNumber(models.Model):
    """Model for tracking phone numbers and their spam likelihood."""

    name = models.CharField(max_length=255, default="Unknown")
    number = models.CharField(max_length=15)
    spam_likelihood = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.number} - {self.name}"


class SpamReport(models.Model):
    """Records actions marking a phone number as spam."""

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="spam_reports")
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, related_name="spam_reports")
    marked_as_spam = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} reported {self.phone_number} as spam"


class UserContact(models.Model):
    """Model to store contact information for each user."""

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="contacts")
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact_name} - {self.contact_number}"
