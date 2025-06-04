from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from faker import Faker
import random
from datetime import date, timedelta

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with sample listings, bookings, and reviews'

    def handle(self, *args, **options):
        # Create test users
        users = []
        for _ in range(3):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='testpass123'
            )
            users.append(user)

        # Create listings
        listings = []
        for _ in range(5):
            listing = Listing.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                price=round(random.uniform(50, 500), 2),
                location=fake.city(),
                owner=random.choice(users)
            )
            listings.append(listing)

        # Create bookings
        bookings = []
        for _ in range(10):
            start_date = fake.date_between(start_date='today', end_date='+30d')
            booking = Booking.objects.create(
                listing=random.choice(listings),
                user=random.choice(users),
                start_date=start_date,
                end_date=start_date + timedelta(days=random.randint(1, 14)),
                status=random.choice(['pending', 'confirmed', 'cancelled'])
            )
            bookings.append(booking)

        # Create reviews for confirmed bookings
        for booking in bookings:
            if booking.status == 'confirmed' and random.choice([True, False]):
                Review.objects.create(
                    booking=booking,
                    rating=random.randint(1, 5),
                    comment=fake.paragraph()
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
