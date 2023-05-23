from . import views
from django.urls import path


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about_us/', views.AboutUs.as_view(), name='about_us'),
    path('menu/', views.Menu.as_view(), name='menu'),


    # BOOKING
    path('bookings/', views.add_booking, name='bookings'),
    path('my_bookings/', views.ShowMyBookings.as_view(), name='my_bookings'),
    path('delete_a_booking/', views.DeleteBooking.as_view(), name='delete_a_booking'),
    path('delete_booking/<booking_id>', views.delete_booking, name='delete_booking'),

]
