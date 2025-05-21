from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from .models import Event
from .forms import SignUpForm, ReservationForm, TripForm
##
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import UserProfile, Trip, Ticket
from .forms import SellerCreationForm
import time
from django.core.exceptions import ObjectDoesNotExist
from .forms import PassengerForm
from django.forms import formset_factory
from django.contrib import messages
from django.utils import timezone
from .forms import UserForm, UserProfileForm, TripReviewForm, SellerTripEditForm




def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout_view(request):
    logout(request)
    return redirect('event_list')

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            if reservation.tickets_reserved <= event.available_tickets:
                event.available_tickets -= reservation.tickets_reserved
                event.save()
                reservation.event = event
                reservation.save()
                return redirect('event_list')
            else:
                form.add_error('tickets_reserved', 'تعداد بلیت کافی موجود نیست.')
    else:
        form = ReservationForm()
    return render(request, 'event_detail.html', {'event': event, 'form': form})

@login_required
def create_trip(request):
    profile = request.user.userprofile
    if profile.role != 'seller' or not profile.company:
        return HttpResponseForbidden("شما اجازه دسترسی به این بخش را ندارید.")
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.company = profile.company
            trip.save()
            return redirect('event_list')
    else:
        form = TripForm()
    return render(request, 'create_trip.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def create_seller_view(request):
    if request.method == 'POST':
        form = SellerCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'این نام کاربری قبلاً استفاده شده است.')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=form.cleaned_data['password']
                )

                for _ in range(5):
                    try:
                        profile = user.userprofile
                        break
                    except ObjectDoesNotExist:
                        time.sleep(0.1)
                else:
                    raise Exception("UserProfile not created by signal")

                profile.phone_number = form.cleaned_data['phone_number']
                profile.role = 'seller'
                profile.company = form.cleaned_data['company']
                profile.save()

    else:
        form = SellerCreationForm()
    return render(request, 'create_seller.html', {'form': form})

def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    return render(request, 'trip_detail.html', {'trip': trip})

def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'ticket_list.html', {'tickets': tickets, "now": timezone.now()})

def seller_tickets(request):
    if not request.user.userprofile.role == 'seller':
        return HttpResponse("شما اجازه دسترسی ندارید")
    company = request.user.userprofile.company
    tickets = Ticket.objects.filter(trip__company=company)
    return render(request, 'ticket_list.html', {'tickets': tickets})

def trip_list(request):
    trips = Trip.objects.all()

    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    departure = request.GET.get('departure_time')
    arrival = request.GET.get('arrival_time')
    i = request.GET.get('arrival_time')

    if origin:
        trips = trips.filter(origin__icontains=origin)
    if destination:
        trips = trips.filter(destination__icontains=destination)
    if departure:
        trips = trips.filter(departure_time__date=departure)
    if arrival:
        trips = trips.filter(arrival_time__date=arrival)

    return render(request, 'trip_list.html', {'trips': trips})

@login_required
def reserve_ticket_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    ticket_count = int(request.POST.get("ticket_count") or request.GET.get("ticket_count") or 1)
    PassengerFormSet = formset_factory(PassengerForm, extra=ticket_count)

    if request.method == "POST":
        formset = PassengerFormSet(request.POST)

        # بررسی ظرفیت باقی‌مانده
        reserved_count = Ticket.objects.filter(trip=trip).count()
        if reserved_count + ticket_count > trip.capacity:
            messages.error(request, "تعداد بلیت‌های درخواستی بیشتر از ظرفیت باقی‌مانده است.")
            return render(request, "reserve_ticket.html", {
                "formset": formset,
                "trip": trip,
                "ticket_count": ticket_count,
            })

        existing_national_codes = set(
            Ticket.objects.filter(trip=trip).values_list("national_code", flat=True)
        )

        entered_codes = []
        has_error = False

        for form in formset:
            if form.is_valid():
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                national_code = form.cleaned_data.get("national_code")
                birth_date = form.cleaned_data.get("birth_date")
                if not first_name:
                    form.add_error("first_name", "وارد کردن نام الزامی است.")
                    has_error = True

                if not last_name:
                    form.add_error("last_name", "وارد کردن نام خانوادگی الزامی است.")
                    has_error = True

                if not birth_date:
                    form.add_error("birth_date", "وارد کردن تاریخ تولد الزامی است.")
                    has_error = True

                if not national_code:
                    form.add_error("national_code", "وارد کردن کد ملی الزامی است.")
                    has_error = True

                elif national_code in entered_codes:
                    form.add_error("national_code", "این کد ملی در فرم‌های بالا تکرار شده است.")
                    has_error = True

                elif national_code in existing_national_codes:
                    form.add_error("national_code", "این کد ملی قبلاً برای این سفر ثبت شده است.")
                    has_error = True

                entered_codes.append(national_code)
            else:
                has_error = True

        if has_error:
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید.")
            return render(request, "reserve_ticket.html", {
                "formset": formset,
                "trip": trip,
                "ticket_count": ticket_count,
            })

        # ذخیره بلیت‌ها
        for form in formset:
            Ticket.objects.create(
                trip=trip,
                user=request.user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                national_code=form.cleaned_data["national_code"],
                birth_date=form.cleaned_data["birth_date"],  # ← جدید
                applied_discount_percent=trip.discount_percent  # ← جدید
            )

        messages.success(request, "رزرو بلیت‌ها با موفقیت انجام شد.")
        return redirect("my_tickets")

    else:
        formset = PassengerFormSet()

    return render(request, "reserve_ticket.html", {
        "formset": formset,
        "trip": trip,
        "ticket_count": ticket_count,
    })

@login_required
def cancel_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if ticket.trip.departure_time <= timezone.now():
        messages.error(request, "امکان لغو بلیت بعد از زمان حرکت وجود ندارد.")
    elif ticket.is_canceled:
        messages.warning(request, "این بلیت قبلاً لغو شده است.")
    else:
        ticket.is_canceled = True
        ticket.save()
        messages.success(request, "بلیت با موفقیت لغو شد.")

    return redirect("my_tickets")

@login_required
def profile_view(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return render(request, 'profile.html', {'user': user, 'profile': profile})

@login_required
def edit_profile_view(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    # فقط ادمین یا خود کاربر بتواند ویرایش کند
    if profile.role != 'admin' and request.user != profile.user:
        return HttpResponseForbidden("شما اجازه دسترسی به این صفحه را ندارید.")

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def cancel_trip_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # بررسی نقش فروشنده
    if user_profile.role != 'seller':
        return HttpResponseForbidden("دسترسی فقط برای فروشندگان مجاز است.")

    # بررسی مالکیت شرکت
    if trip.company != user_profile.company:
        return HttpResponseForbidden("شما اجازه لغو این سفر را ندارید.")

    # بررسی اینکه هنوز سفر شروع نشده
    if trip.departure_time <= timezone.now():
        messages.error(request, "امکان لغو سفر پس از زمان حرکت وجود ندارد.")
        return redirect('trip_list')  # مسیر مناسب را جایگزین کن

    # کنسل کردن همه بلیت‌ها
    Ticket.objects.filter(trip=trip).update(is_canceled=True, is_canceled_by_company=True)

    messages.success(request, "سفر با موفقیت لغو شد و بلیت‌های آن نیز کنسل شدند.")
    return redirect('trip_list')  # مسیر مناسب را جایگزین کن

@login_required
def add_review_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = TripReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.trip = trip
            review.user = request.user
            review.role = user_profile.role
            review.save()
            messages.success(request, "نظر شما با موفقیت ثبت شد.")
            return redirect('trip_detail', trip_id=trip.id)  # یا مسیر مناسب
    else:
        form = TripReviewForm()

    return render(request, 'add_review.html', {'form': form, 'trip': trip})

@login_required
def seller_edit_trip_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.role != 'seller' or trip.company != user_profile.company:
        return HttpResponseForbidden("شما اجازه ویرایش این سفر را ندارید.")

    if trip.departure_time <= timezone.now():
        return HttpResponseForbidden("امکان ویرایش سفر پس از زمان حرکت وجود ندارد.")

    if request.method == 'POST':
        form = SellerTripEditForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات سفر با موفقیت ویرایش شد.")
            return redirect('trip_detail', trip_id=trip.id)
    else:
        form = SellerTripEditForm(instance=trip)

    return render(request, 'seller_edit_trip.html', {'form': form, 'trip': trip})








