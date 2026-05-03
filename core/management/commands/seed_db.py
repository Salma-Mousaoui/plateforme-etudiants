"""
Management command: seed_db
Populates the database with realistic test data for every platform feature.

Usage:
    # Add data without touching existing records
    python manage.py seed_db

    # Wipe all non-superuser data, then reseed from scratch
    python manage.py seed_db --flush
"""

import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from faker import Faker

from chat.models import ChatGroup, Message
from core.models import ProfessionalProfile
from housing.models import HousingListing
from reports.models import Report

User = get_user_model()
fake = Faker("fr_FR")

CITIES = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Granada"]

LAWYER_SPECIALITIES = [
    "Immigration law", "Student visa", "Residence permit",
    "Family reunification", "Work permit",
]
ADVISOR_SPECIALITIES = [
    "University admissions", "Scholarships", "Master's programs",
    "Engineering schools", "Medical studies",
]
LANGUAGES_OPTIONS = [
    "Arabic, French, Spanish",
    "French, Spanish, English",
    "Arabic, Spanish",
    "French, Spanish",
    "Arabic, French, Spanish, English",
]
REASONS = ["scam", "inappropriate_behavior", "fake_profile", "other"]

GROUP_MESSAGES = [
    "Hi everyone, anyone knows a good landlord here?",
    "Looking for a roommate starting September",
    "What's the best district near the university?",
    "Anyone else struggling with the NIE process?",
    "Does anyone know a good affordable area to live?",
    "Just arrived last week, any tips for newcomers?",
    "Looking for study partners for the exam session",
    "Anyone in the same faculty?",
    "Is there a WhatsApp group for Moroccan students here?",
    "What's the cheapest supermarket near campus?",
    "Does anyone know how to register for health insurance?",
    "Looking for a furnished room under 400€",
    "Anyone going back to Morocco for summer?",
    "Study group at the library this weekend?",
    "New to the city — where should I start looking for housing?",
]

PRIVATE_MESSAGES = [
    "Hey, I saw your listing — is it still available?",
    "Hi, could you help me with my visa application?",
    "I'm interested in the room you posted, can we talk?",
    "Hello! I found your profile on Elan, I need legal advice.",
    "Hi, I'm a new student in the city. Any tips?",
    "I'd like to schedule a consultation with you.",
    "Can you tell me more about the apartment?",
    "Hi! I need help with university admission paperwork.",
    "Is the shared housing near the metro?",
    "Thanks for the advice last time, it really helped!",
]


class Command(BaseCommand):
    help = "Seed the database with test data for all platform features"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing non-superuser data before seeding",
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            if options["flush"]:
                self._flush()

            self._create_admin()
            students = self._create_students()
            validated_lawyers, pending_lawyers = self._create_professionals(
                prefix="lawyer", role="lawyer", total=8, n_validated=5,
                specialities=LAWYER_SPECIALITIES, password="Lawyer1234!",
            )
            validated_advisors, pending_advisors = self._create_professionals(
                prefix="advisor", role="orientation", total=6, n_validated=4,
                specialities=ADVISOR_SPECIALITIES, password="Advisor1234!",
            )
            validated_owners, pending_owners = self._create_owners()
            listings = self._create_listings(validated_owners)
            groups = self._create_chat_groups(students)
            group_msgs, private_msgs = self._create_messages(
                students, validated_lawyers + validated_advisors, groups
            )
            reports = self._create_reports(
                students,
                [l for l in listings if l.is_approved and l.is_active],
                validated_lawyers + validated_advisors,
            )

            self._print_summary(
                n_lawyers=len(validated_lawyers) + len(pending_lawyers),
                vl=len(validated_lawyers), pl=len(pending_lawyers),
                n_advisors=len(validated_advisors) + len(pending_advisors),
                va=len(validated_advisors), pa=len(pending_advisors),
                n_owners=len(validated_owners) + len(pending_owners),
                vo=len(validated_owners), po=len(pending_owners),
                n_listings=len(listings),
                approved=[l for l in listings if l.is_approved and l.is_active],
                pending=[l for l in listings if not l.is_approved],
                n_group_msgs=len(group_msgs),
                n_private_msgs=len(private_msgs),
                reports=reports,
            )

    # ------------------------------------------------------------------ #
    #  FLUSH                                                               #
    # ------------------------------------------------------------------ #

    def _flush(self):
        Message.objects.all().delete()
        ChatGroup.objects.all().delete()
        Report.objects.all().delete()
        HousingListing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write("[FLUSH] Database flushed.")

    # ------------------------------------------------------------------ #
    #  USERS                                                               #
    # ------------------------------------------------------------------ #

    def _create_admin(self):
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@plateforme.com",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
                "is_validated": True,
                "is_active": True,
            },
        )
        if created:
            user.set_password("Admin1234!")
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "[OK] Admin created -- login: admin@plateforme.com / Admin1234!"
                )
            )
        else:
            self.stdout.write("[SKIP] Admin already exists, skipping")

    def _create_students(self):
        students = []
        for i in range(1, 21):
            user, created = User.objects.get_or_create(
                email=f"student{i}@test.com",
                defaults={
                    "username": f"student{i}",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "role": "student",
                    "is_active": True,
                    "is_validated": True,
                    "city": random.choice(CITIES),
                    "phone": fake.phone_number()[:30],
                },
            )
            if created:
                user.set_password("Student1234!")
                user.save()
            students.append(user)
        return students

    def _create_professionals(self, prefix, role, total, n_validated, specialities, password):
        validated, pending = [], []
        for i in range(1, total + 1):
            is_val = i <= n_validated
            user, created = User.objects.get_or_create(
                email=f"{prefix}{i}@test.com",
                defaults={
                    "username": f"{prefix}{i}",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "role": role,
                    "is_active": is_val,
                    "is_validated": is_val,
                    "city": random.choice(CITIES),
                    "phone": fake.phone_number()[:30],
                },
            )
            if created:
                user.set_password(password)
                user.save()
            ProfessionalProfile.objects.update_or_create(
                user=user,
                defaults={
                    "bio": fake.paragraph(nb_sentences=4),
                    "speciality": random.choice(specialities),
                    "languages": random.choice(LANGUAGES_OPTIONS),
                    "website": fake.url(),
                },
            )
            (validated if is_val else pending).append(user)
        return validated, pending

    def _create_owners(self):
        validated, pending = [], []
        for i in range(1, 6):
            is_val = i <= 4
            user, created = User.objects.get_or_create(
                email=f"owner{i}@test.com",
                defaults={
                    "username": f"owner{i}",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "role": "housing",
                    "is_active": is_val,
                    "is_validated": is_val,
                    "city": random.choice(CITIES),
                    "phone": fake.phone_number()[:30],
                },
            )
            if created:
                user.set_password("Owner1234!")
                user.save()
            (validated if is_val else pending).append(user)
        return validated, pending

    # ------------------------------------------------------------------ #
    #  LISTINGS                                                            #
    # ------------------------------------------------------------------ #

    def _listing_title(self, listing_type, city):
        templates = {
            "chambre": [
                f"Bright room near {city} university",
                f"Furnished room in {city} center",
                f"Quiet room close to campus — {city}",
                f"Single room in shared flat — {city}",
                f"Sunny bedroom near metro — {city}",
            ],
            "appartement": [
                f"Furnished apartment in {city} center",
                f"Modern studio apartment — {city}",
                f"Cozy 2-room apartment near {city} university",
                f"Bright apartment with balcony — {city}",
                f"Fully equipped flat — {city}",
            ],
            "colocation": [
                f"Shared housing 4 rooms — close to {city} campus",
                f"Coliving space for students — {city}",
                f"Shared flat 3 bedrooms — {city} center",
                f"Student colocation near {city} metro",
                f"Roommates wanted — {city}",
            ],
        }
        return random.choice(templates[listing_type])

    def _create_listings(self, validated_owners):
        # Controlled distributions
        types = ["chambre"] * 10 + ["appartement"] * 10 + ["colocation"] * 10
        random.shuffle(types)

        prices = (
            [round(random.uniform(200, 400), 2) for _ in range(10)]
            + [round(random.uniform(400, 700), 2) for _ in range(10)]
            + [round(random.uniform(700, 1200), 2) for _ in range(10)]
        )
        random.shuffle(prices)

        # At least 4 listings per city (5 × 4 = 20) + 10 random
        cities = CITIES * 4 + [random.choice(CITIES) for _ in range(10)]
        random.shuffle(cities)

        # 22 approved+active, 6 pending, 2 approved+inactive
        statuses = [(True, True)] * 22 + [(False, True)] * 6 + [(True, False)] * 2
        random.shuffle(statuses)

        to_create = []
        for i in range(30):
            is_approved, is_active = statuses[i]
            to_create.append(
                HousingListing(
                    owner=random.choice(validated_owners),
                    title=self._listing_title(types[i], cities[i]),
                    description=fake.paragraph(nb_sentences=6),
                    type=types[i],
                    price=prices[i],
                    city=cities[i],
                    is_approved=is_approved,
                    is_active=is_active,
                )
            )

        created = HousingListing.objects.bulk_create(to_create)

        # Backdate created_at (auto_now_add prevents setting it on creation)
        for listing in created:
            HousingListing.objects.filter(pk=listing.pk).update(
                created_at=timezone.now() - timedelta(days=random.randint(0, 60))
            )

        return list(HousingListing.objects.filter(pk__in=[l.pk for l in created]))

    # ------------------------------------------------------------------ #
    #  CHAT                                                                #
    # ------------------------------------------------------------------ #

    def _create_chat_groups(self, students):
        groups = []
        for city in CITIES:
            group, _ = ChatGroup.objects.get_or_create(
                name=f"Students in {city}",
                defaults={"city": city},
            )
            city_students = [s for s in students if s.city == city]
            if city_students:
                group.members.add(*city_students)
            groups.append(group)
        return groups

    def _create_messages(self, students, pros, groups):
        now = timezone.now()
        group_msgs, private_msgs = [], []

        # 3 group messages per group = 15 total
        for idx, group in enumerate(groups):
            members = list(group.members.all()) or students[:3]
            for j in range(3):
                msg = Message.objects.create(
                    sender=random.choice(members),
                    group=group,
                    content=GROUP_MESSAGES[(idx * 3 + j) % len(GROUP_MESSAGES)],
                )
                Message.objects.filter(pk=msg.pk).update(
                    sent_at=now - timedelta(days=random.randint(0, 7))
                )
                group_msgs.append(msg)

        # 10 private messages
        all_recipients = students + pros
        for j in range(10):
            sender = random.choice(students)
            receiver = random.choice([u for u in all_recipients if u != sender])
            msg = Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=PRIVATE_MESSAGES[j % len(PRIVATE_MESSAGES)],
            )
            Message.objects.filter(pk=msg.pk).update(
                sent_at=now - timedelta(days=random.randint(0, 14))
            )
            private_msgs.append(msg)

        return group_msgs, private_msgs

    # ------------------------------------------------------------------ #
    #  REPORTS                                                             #
    # ------------------------------------------------------------------ #

    def _create_reports(self, students, approved_listings, pros):
        # 8 reports: 6 pending + 2 resolved, assigned sequentially
        statuses = ["pending"] * 6 + ["resolved"] * 2
        reports = []
        idx = 0

        # 3 reports on listings
        for listing in random.sample(approved_listings, min(3, len(approved_listings))):
            r = Report.objects.create(
                reporter=random.choice(students),
                listing=listing,
                reason=random.choice(REASONS),
                description=fake.sentence(),
                status=statuses[idx],
            )
            reports.append(r)
            idx += 1

        # 3 reports on professionals
        for pro in random.sample(pros, min(3, len(pros))):
            r = Report.objects.create(
                reporter=random.choice(students),
                reported_user=pro,
                reason=random.choice(REASONS),
                description=fake.sentence(),
                status=statuses[idx],
            )
            reports.append(r)
            idx += 1

        # 2 more (1 listing + 1 pro) to reach 8 total and exhaust statuses
        if approved_listings:
            r = Report.objects.create(
                reporter=random.choice(students),
                listing=random.choice(approved_listings),
                reason=random.choice(REASONS),
                description=fake.sentence(),
                status=statuses[idx],
            )
            reports.append(r)
            idx += 1

        if pros and idx < len(statuses):
            r = Report.objects.create(
                reporter=random.choice(students),
                reported_user=random.choice(pros),
                reason=random.choice(REASONS),
                description=fake.sentence(),
                status=statuses[idx],
            )
            reports.append(r)

        return reports

    # ------------------------------------------------------------------ #
    #  SUMMARY                                                             #
    # ------------------------------------------------------------------ #

    def _print_summary(
        self, n_lawyers, vl, pl, n_advisors, va, pa,
        n_owners, vo, po, n_listings, approved, pending,
        n_group_msgs, n_private_msgs, reports,
    ):
        n_pending_reports = sum(1 for r in reports if r.status == "pending")
        n_resolved_reports = sum(1 for r in reports if r.status == "resolved")

        sep = "=" * 47
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(sep))
        self.stdout.write(self.style.SUCCESS("  DATABASE SEEDED SUCCESSFULLY"))
        self.stdout.write(self.style.SUCCESS(sep))
        self.stdout.write(self.style.SUCCESS(f"  Admins:      1"))
        self.stdout.write(self.style.SUCCESS(f"  Students:    20"))
        self.stdout.write(self.style.SUCCESS(f"  Lawyers:     {n_lawyers} ({vl} validated, {pl} pending)"))
        self.stdout.write(self.style.SUCCESS(f"  Advisors:    {n_advisors} ({va} validated, {pa} pending)"))
        self.stdout.write(self.style.SUCCESS(f"  Owners:      {n_owners} ({vo} validated, {po} pending)"))
        self.stdout.write(self.style.SUCCESS(f"  Listings:    {n_listings} ({len(approved)} approved, {len(pending)} pending)"))
        self.stdout.write(self.style.SUCCESS(f"  Chat Groups: 5"))
        self.stdout.write(self.style.SUCCESS(f"  Messages:    {n_group_msgs + n_private_msgs} ({n_group_msgs} group + {n_private_msgs} private)"))
        self.stdout.write(self.style.SUCCESS(f"  Reports:     {len(reports)} ({n_pending_reports} pending, {n_resolved_reports} resolved)"))
        self.stdout.write(self.style.SUCCESS(sep))
        self.stdout.write("")
        self.stdout.write("TEST CREDENTIALS:")
        self.stdout.write("  Admin:   admin@plateforme.com  / Admin1234!")
        self.stdout.write("  Student: student1@test.com     / Student1234!")
        self.stdout.write("  Lawyer:  lawyer1@test.com      / Lawyer1234!")
        self.stdout.write("  Advisor: advisor1@test.com     / Advisor1234!")
        self.stdout.write("  Owner:   owner1@test.com       / Owner1234!")
        self.stdout.write("")
