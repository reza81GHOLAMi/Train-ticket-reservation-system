from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Trip, UserProfile, Company, Ticket, TripReview
from django.core.exceptions import ValidationError
from django.utils import timezone

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if UserProfile.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("این شماره همراه قبلاً ثبت شده است.")
        return phone

    def save(self, commit=True):
        user = super().save(commit)
        phone_number = self.cleaned_data['phone_number']
        profile = user.userprofile
        profile.phone_number = phone_number
        profile.save()
        return user

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'tickets_reserved']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['train_number', 'capacity', 'origin', 'destination',
                  'departure_time', 'arrival_time', 'ticket_price']

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get('origin')
        destination = cleaned_data.get('destination')
        departure = cleaned_data.get('departure_time')
        arrival = cleaned_data.get('arrival_time')
        if origin and destination and origin == destination:
            raise ValidationError("مبدا و مقصد نمی تواند یکسان باشد.")
        if departure and arrival and departure <= timezone.now():
            raise ValidationError("تاریخ حرکت باید بعد از تاریخ حال حاضر باشد.")
        if departure and arrival and arrival <= departure:
            raise ValidationError("تاریخ رسیدن باید بعد از تاریخ حرکت باشد.")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'role', 'company']

class SellerCreationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=11)
    company = forms.ModelChoiceField(queryset=Company.objects.all())

class TicketReservationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['first_name', 'last_name', 'national_code', 'birth_date']  # ← اضافه شده
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PassengerForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="نام")
    last_name = forms.CharField(max_length=50, label="نام خانوادگی")
    national_code = forms.CharField(max_length=10, label="کد ملی")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class TripReviewForm(forms.ModelForm):
    class Meta:
        model = TripReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class SellerTripEditForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['ticket_price', 'catering_description', 'discount_percent']
        widgets = {
            'discount_percent': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }


