from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'مشتری'),
        ('seller', 'فروشنده'),
        ('admin', 'ادمین'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    available_tickets = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    tickets_reserved = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class Trip(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)
    train_number = models.CharField(max_length=20, null=False)
    capacity = models.PositiveIntegerField(null=False)
    origin = models.CharField(max_length=100, null=False)
    destination = models.CharField(max_length=100,null=False)
    departure_time = models.DateTimeField(null=False)
    arrival_time = models.DateTimeField(null=False)
    ticket_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.train_number} | {self.origin} → {self.destination} ({self.departure_time})"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    national_code = models.CharField(max_length=10, null=False)
    is_canceled = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.trip.train_number} "


