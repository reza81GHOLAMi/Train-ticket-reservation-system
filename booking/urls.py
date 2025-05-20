from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('trips/create/', views.create_trip, name='create_trip'),
    path('create-seller/', views.create_seller_view, name='create_seller'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('seller-tickets/', views.seller_tickets, name='seller_tickets'),
    path('trips/', views.trip_list, name='trip_list'),
    path("trip/<int:trip_id>/reserve/", views.reserve_ticket_view, name="reserve_ticket"),
    path("ticket/<int:ticket_id>/cancel/", views.cancel_ticket, name="cancel_ticket"),
]
