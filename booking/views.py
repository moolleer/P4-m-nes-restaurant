from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking, Table
from .forms import BookingForm


class Home(generic.TemplateView):
    """Open landing page"""
    template_name = "index.html"


class AboutUs(generic.TemplateView):
    """Open About us page"""
    template_name = "about_us.html"


class Menu(generic.TemplateView):
    """Open Menu page"""
    template_name = "menu.html"


class DeleteBooking(generic.TemplateView):
    """Open Delete a booking page"""
    template_name = "delete_a_booking.html"


class ShowMyBookings(generic.ListView):
    """Show the users bookings"""
    model = Booking
    template_name = 'my_bookings.html'

    def get_queryset(self):
        return Booking.objects.filter(booked_by=self.request.user)


@login_required()
def add_booking(request):
    """
    Allows a user to make a booking, and checks
    if a table is available for the amount of guests,
    and requested day and time. Also prevent users
    from making more than one booking on the same day.
    """

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data['date']
            booking_time = form.cleaned_data['time']

            booking = form.save(commit=False)
            booking.booked_by = request.user

            # Check if any available tables
            if booking.assign_table():
                booking.save()
                messages.success(request, 'Booking completed')
                return redirect(reverse('my_bookings'))

            else:
                messages.error(
                    request,
                    'No more available tables for this day and time.'
                )
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


@login_required()
def delete_booking(request, booking_id):
    """
    Users can choose to delete a booking. The delete booking
    page give the users information that this cant be undone,
    and if they chose cancel they will be redirected back to my bookings.
    If they click on the delete button the booking will be
    deleted permanently.
    """
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method == "POST":
        booking.delete()
        messages.success(request, 'Your booking has been deleted!')
        return redirect(reverse('my_bookings'))

    template = 'delete_a_booking.html'
    context = {
        'booking': booking,
    }

    return render(request, template, context)


@login_required()
def edit_booking(request, booking_id):
    """
    Users can edit their bookings time, date,
    and number of persons. Initializes the form
    with the form data and the existing booking instance,
    checks if the form is valid and if so save it.

    """
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)

            if booking.assign_table():
                booking.save()
                messages.success(request, 'Your booking has been updated')
                return redirect('my_bookings')
            else:
                messages.error(
                    request, 'No more available tables for this day and time.')
    else:
        form = BookingForm(instance=booking)

    template = 'edit_booking.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
