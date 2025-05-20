from django.contrib import admin
from .models import Company, UserProfile, Trip, Event, Reservation, Ticket

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'company')
    list_filter = ('role', 'company')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'train_number',
        'origin',
        'destination',
        'departure_time',
        'arrival_time',
        'capacity',
        'ticket_price'
    )
    list_filter = ('company', 'departure_time', 'arrival_time')
    search_fields = ('train_number', 'origin', 'destination')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'available_tickets')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'tickets_reserved')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'national_code', 'trip', 'user')
    list_filter = ('trip', 'user')
    search_fields = ('first_name', 'last_name', 'national_code', 'user__username')

