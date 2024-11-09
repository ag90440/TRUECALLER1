import random
from django.core.management.base import BaseCommand
from identifyCallerApp.models import AppUser, UserContact, PhoneNumber


class Command(BaseCommand):
    help = 'Populates the database with sample data for testing purposes'

    def handle(self, *args, **options):
        # Retain a specific user if present; delete others
        admin_phone = '1234567890'
        admin_user = AppUser.objects.filter(phone_number=admin_phone).first()
        if admin_user:
            AppUser.objects.exclude(id=admin_user.id).delete()
        else:
            admin_user = AppUser.objects.create_user(
                name='Admin User',
                phone_number=admin_phone,
                email='admin@example.com',
                password='adminpass'
            )

        # Clear related tables
        UserContact.objects.all().delete()
        PhoneNumber.objects.all().delete()

        # Generate sample users and data
        for _ in range(50):  # Number of users to generate
            user = AppUser.objects.create_user(
                name=f'User{random.randint(1, 1000)}',
                phone_number=f'{random.randint(1000000000, 9999999999)}',
                email=f'user{random.randint(1, 1000)}@example.com',
                password='userpass123'
            )

            # Generate contacts for each user
            for _ in range(random.randint(1, 5)):
                UserContact.objects.create(
                    user=user,
                    contact_name=f'Contact{random.randint(1, 1000)}',
                    contact_number=f'{random.randint(1000000000, 9999999999)}'
                )

            # Generate phone numbers with spam likelihoods
            for _ in range(random.randint(1, 5)):
                PhoneNumber.objects.create(
                    name=f'Number{random.randint(1, 1000)}',
                    number=f'{random.randint(1000000000, 9999999999)}',
                    spam_likelihood=random.randint(0, 100)
                )

        self.stdout.write(self.style.SUCCESS('Sample data successfully added to the database.'))
