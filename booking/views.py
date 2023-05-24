from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import Booking, Table
from .forms import BookingForm


class Home(generic.TemplateView):
    """Opens to landing page"""
    template_name = "index.html"


class AboutUs(generic.TemplateView):
    """Opens to About us page"""
    template_name = "about_us.html"


class Menu(generic.TemplateView):
    """Opens to Menu page"""
    template_name = "menu.html"


class DeleteBooking(generic.TemplateView):
    """Opens Delete a booking page"""
    template_name = "delete_a_booking.html"


class ShowMyBookings(generic.ListView):
    """Show the users bookings"""
    model = Booking
    template_name = 'my_bookings.html'

    def get_queryset(self):
        return Booking.objects.filter(booked_by=self.request.user)


def add_booking(request):
    """
    Allows a user to make a booking, and checks
    if a table is available for the amount of guests,
    and requested day and time.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.booked_by = request.user

            if booking.assign_table():
                booking.save()
                messages.success(request, 'Booking completed')
                return redirect(reverse('my_bookings'))
            else:
                messages.error(
                    request, 'No more available tables for this day and time.')
        else:
            messages.error(
                request, 'An error occurred, please try again')
    else:
        form = BookingForm()

    template = 'bookings.html'
    context = {
        'form': form
    }

    return render(request, template, context)


def delete_booking(request, booking_id):
    """

    """
    booking = get_object_or_404(Booking, booking_id=booking_id)
    print(booking_id)
    if request.method == "POST":
        booking.delete()
        messages.success(request, 'Your booking has been deleted!')
        return redirect(reverse('my_bookings'))

    template = 'delete_a_booking.html'
    context = {
        'booking': booking,
    }

    return render(request, template, context)
