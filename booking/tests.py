from random import random

from booking.models import UserProfile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Trip, Ticket, UserProfile, Company
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command



'''
class SignupTest(TestCase):
    def test_signup_creates_user_and_profile(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'phone_number': '09123456789',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

class SigninTest(TestCase):
    def setUp(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser2',
            'email': 'newuser@example.com',
            'phone_number': '09123456789',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
    def test_login_success(self):

        response = self.client.post(reverse('signin'), {
            'username': 'newuser2',
            'password': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('event_list'))

    def test_login_failure(self):
        response = self.client.post(reverse('signin'), {
            'username': 'newuser',
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)
        ##self.assertContains(response, "")

class TripCreationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(name="قطار شرق")
        
        self.admin = User.objects.create_superuser(username="admin", password="admin")
        self.admin.userprofile.phone_number = f"091210008"
        self.admin.userprofile.save()

        # test_customer_cannot_create_trip
        #########################################
        self.client.post(reverse('signup'), {
            'username': 'newuser2',
            'email': 'newuser@example.com',
            'phone_number': '09123456789',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        #########################################

        self.client.login(username="admin", password="admin")
        self.client.post(reverse('create_seller'),{
            'username': 'rezareza',
            'password': '1234',
            'phone_number': '091210009',
            'company' : self.company.id,
        })

        self.client.post(reverse('signin'), {
            'username': 'rezareza',
            'password': '1234',
        })

        self.url = reverse('create_trip')

    def test_seller_can_create_trip(self):

        response = self.client.post(self.url, {
            'train_number': 'T123',
            'capacity': 100,
            'origin': 'تهران',
            'destination': 'مشهد',
            'departure_time': timezone.now() + timedelta(days=1),
            'arrival_time': timezone.now() + timedelta(days=2),
            'ticket_price': 50000,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Trip.objects.count(), 1)


    def test_customer_cannot_create_trip(self):
        self.client.post(reverse('signin'), {
            'username': 'newuser2',
            'password': 'TestPassword123',
        })
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Trip.objects.count(), 0)

    def test_invalid_times_raise_error_arrival_time(self):
        self.client.login(username="rezareza", password="1234")
        response = self.client.post(self.url, {
            'train_number': 'T999',
            'capacity': 100,
            'origin': 'تهران',
            'destination': 'تبریز',
            'departure_time': timezone.now() + timedelta(days=2),
            'arrival_time': timezone.now() + timedelta(days=1),
            'ticket_price': 75000,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "تاریخ رسیدن باید بعد از تاریخ حرکت باشد.")
        self.assertEqual(Trip.objects.count(), 0)

    def test_invalid_times_raise_error_departure_time(self):
        self.client.login(username="rezareza", password="1234")
        response = self.client.post(self.url, {
            'train_number': 'T999',
            'capacity': 100,
            'origin': 'تهران',
            'destination': 'تبریز',
            'departure_time': timezone.now() - timedelta(days=2),
            'arrival_time': timezone.now() + timedelta(days=1),
            'ticket_price': 75000,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "تاریخ حرکت باید بعد از تاریخ حال حاضر باشد.")
        self.assertEqual(Trip.objects.count(), 0)

    def test_invalid_origin_destination(self):
        self.client.login(username="rezareza", password="1234")
        response = self.client.post(self.url, {
            'train_number': 'T999',
            'capacity': 100,
            'origin': 'تهران',
            'destination': 'تهران',
            'departure_time': timezone.now() + timedelta(days=2),
            'arrival_time': timezone.now() + timedelta(days=3),
            'ticket_price': 75000,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "مبدا و مقصد نمی تواند یکسان باشد.")
        self.assertEqual(Trip.objects.count(), 0)
'''
class TicketReservationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(name="Test Company")

        self.admin = User.objects.create_superuser(username="admin", password="admin")
        self.admin.userprofile.phone_number = f"091210008"
        self.admin.userprofile.save()

        self.client.login(username="admin", password="admin")
        self.client.post(reverse('create_seller'), {
            'username': 'seller',
            'password': '1234',
            'phone_number': '091210009',
            'company': self.company.id,
        })
        self.client.post(reverse('signup'), {
            'username': 'tester',
            'email': 'tester@example.com',
            'phone_number': '091289',
            'password1': '12345',
            'password2': '12345',
        })
        self.client.post(reverse('signup'), {
            'username': 'newuser2',
            'email': 'newuser@example.com',
            'phone_number': '09123456789',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        '''
        self.trip = Trip.objects.create(
            train_number="T100",
            company=self.company,
            capacity=10,
            origin="Tehran",
            destination="Mashhad",
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=2),
            ticket_price=50000,
        )
        '''
        call_command('loaddata', 'myfixture')
        self.url = reverse('reserve_ticket', args=[self.trip.id])
        self.client.login(username="tester", password="12345")


    def test_user_can_reserve_two_tickets_successfully(self):
        response = self.client.post(self.url, {
            'ticket_count': 2,
            'form-0-first_name': 'Ali',
            'form-0-last_name': 'Ahmadi',
            'form-0-national_code': '1234567890',
            'form-1-first_name': 'Sara',
            'form-1-last_name': 'Karimi',
            'form-1-national_code': '9876543210',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 2)


    def test_reservation_fails_due_to_over_capacity(self):
        self.trip.capacity = 1
        self.trip.save()
        response = self.client.post(self.url, {
            'ticket_count': 2,
            'form-0-first_name': 'Ali',
            'form-0-last_name': 'Ahmadi',
            'form-0-national_code': '1234567890',
            'form-1-first_name': 'Sara',
            'form-1-last_name': 'Karimi',
            'form-1-national_code': '9876543210',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ticket.objects.count(), 0)
        self.assertContains(response, "تعداد بلیت‌های درخواستی بیشتر از ظرفیت باقی‌مانده است.")

    def test_reservation_fails_due_to_missing_fields(self):
        response = self.client.post(self.url, {
            'ticket_count': 2,
            'form-0-first_name': '',
            'form-0-last_name': '',
            'form-0-national_code': '',
            'form-1-first_name': 'Sara',
            'form-1-last_name': 'Karimi',
            'form-1-national_code': '9876543210',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        })
        self.assertContains(response, "الزامی است")
        self.assertEqual(Ticket.objects.count(), 0)

    def test_reservation_fails_due_to_duplicate_national_codes(self):
        response = self.client.post(self.url, {
            'ticket_count': 2,
            'form-0-first_name': 'Ali',
            'form-0-last_name': 'Ahmadi',
            'form-0-national_code': '1234567890',
            'form-1-first_name': 'Sara',
            'form-1-last_name': 'Karimi',
            'form-1-national_code': '1234567890',  # تکراری
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        })
        self.assertContains(response, "تکرار شده است")
        self.assertEqual(Ticket.objects.count(), 0)

    def test_customer_sees_only_their_tickets(self):
        self.client.post(self.url, {
            'ticket_count': 2,
            'form-0-first_name': 'Ali',
            'form-0-last_name': 'Ahmadi',
            'form-0-national_code': '1234567890',
            'form-1-first_name': 'Sara',
            'form-1-last_name': 'Karimi',
            'form-1-national_code': '9876543210',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        })
        self.client.login(username="newuser2", password="TestPassword123")
        self.client.post(self.url, {
            'ticket_count': 2,
            'form-0-first_name': 'reza',
            'form-0-last_name': 'rezaie',
            'form-0-national_code': '125680',
            'form-1-first_name': 'Sadra',
            'form-1-last_name': 'sadeghi',
            'form-1-national_code': '954310',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        })
        self.assertEqual(Ticket.objects.count(), 4)
        response = self.client.get(reverse('my_tickets'))
        self.assertContains(response, "Sadra")
        self.assertContains(response, "sadeghi")
        self.assertNotContains(response, "Karimi")
        self.assertNotContains(response, "Sara")

    def test_seller_sees_tickets_for_their_company_trips(self):
        self.client.post(self.url, {
            'ticket_count': 2,
            'form-0-first_name': 'Ali',
            'form-0-last_name': 'Ahmadi',
            'form-0-national_code': '1234567890',
            'form-1-first_name': 'Sara',
            'form-1-last_name': 'Karimi',
            'form-1-national_code': '9876543210',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        })
        self.client.login(username="newuser2", password="TestPassword123")
        self.client.post(self.url, {
            'ticket_count': 2,
            'form-0-first_name': 'reza',
            'form-0-last_name': 'rezaie',
            'form-0-national_code': '125680',
            'form-1-first_name': 'Sadra',
            'form-1-last_name': 'sadeghi',
            'form-1-national_code': '954310',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        })
        self.client.login(username="seller", password="1234")
        response = self.client.get(reverse('seller_tickets'))
        self.assertEqual(len(response.context["tickets"]), 4)
        self.assertContains(response, "Sadra")
        self.assertContains(response, "Ali")
'''
class TripFilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        company = Company.objects.create(name="ریل کویر")

        Trip.objects.create(
            company=company,
            train_number="T101",
            capacity=100,
            origin="تهران",
            destination="مشهد",
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=2),
            ticket_price=50000
        )

        Trip.objects.create(
            company=company,
            train_number="T202",
            capacity=80,
            origin="اصفهان",
            destination="شیراز",
            departure_time=timezone.now() + timedelta(days=3),
            arrival_time=timezone.now() + timedelta(days=4),
            ticket_price=60000
        )

    def test_filter_by_origin_and_destination(self):
        response = self.client.get(reverse('trip_list'), {
            'origin': 'تهران',
            'destination': 'مشهد',
        })
        self.assertContains(response, "T101")
        self.assertNotContains(response, "T202")


    def test_filter_by_departure_date(self):
        target_date = (timezone.now() + timedelta(days=1)).date().isoformat()
        response = self.client.get(reverse('trip_list'), {
            'departure_time': target_date
        })
        self.assertContains(response, "T101")
        self.assertNotContains(response, "T202")

    def test_filter_by_arrival_date(self):
        target_date = (timezone.now() + timedelta(days=4)).date().isoformat()
        response = self.client.get(reverse('trip_list'), {
            'arrival_time': target_date
        })
        self.assertContains(response, "T202")
        self.assertNotContains(response, "T101")

class TicketCancelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post(reverse('signup'), {
            'username': 'tester',
            'email': 'tester@example.com',
            'phone_number': '091289',
            'password1': '1234',
            'password2': '1234',
        })
        self.company = Company.objects.create(name="Test Co")
        self.client.login(username="tester", password="1234")
        self.user = User.objects.filter(username="tester").first()
        self.trip_future = Trip.objects.create(
            train_number="T200",
            company=self.company,
            capacity=100,
            origin="Tehran",
            destination="Isfahan",
            departure_time=timezone.now() + timedelta(days=2),
            arrival_time=timezone.now() + timedelta(days=3),
            ticket_price=100000,
        )

        self.trip_past = Trip.objects.create(
            train_number="T201",
            company=self.company,
            capacity=100,
            origin="Tehran",
            destination="Shiraz",
            departure_time=timezone.now() - timedelta(days=2),
            arrival_time=timezone.now() - timedelta(days=1),
            ticket_price=90000,
        )

        self.ticket_future = Ticket.objects.create(
            trip=self.trip_future,
            user=self.user,
            first_name="Ali",
            last_name="Rezaei",
            national_code="1234567890"
        )

        self.ticket_past = Ticket.objects.create(
            trip=self.trip_past,
            user=self.user,
            first_name="Sara",
            last_name="Karimi",
            national_code="9876543210"
        )

    def test_successful_ticket_cancel(self):
        url = reverse('cancel_ticket', args=[self.ticket_future.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('my_tickets'))

        self.ticket_future.refresh_from_db()
        self.assertTrue(self.ticket_future.is_canceled)

    def test_unsuccessful_ticket_cancel_due_to_past_departure(self):
        url = reverse('cancel_ticket', args=[self.ticket_past.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('my_tickets'))

        self.ticket_past.refresh_from_db()
        self.assertFalse(self.ticket_past.is_canceled)
'''