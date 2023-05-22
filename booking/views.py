from django.shortcuts import render, reverse, redirect
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import Booking
from .forms import BookingForm


class Home(generic.TemplateView):
    """Opens to landing page"""
    template_name = "index.html"


class AboutUs(generic.TemplateView):
    """Opens to About us page"""
    template_name = "about_us.html"


class Menu(generic.TemplateView):
    """Opens to Menu us page"""
    template_name = "menu.html"


class ShowMyBookings(generic.ListView):
    """Show the users bookings"""
    model = Booking
    template_name = 'my_bookings.html'
    paginate_by = 6

    def get_queryset(self):
        return Booking.objects.filter(booked_by=self.request.user)


def add_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.instance.booked_by = request.user
            form.save()
            messages.success(request, 'Booking completed')
            return redirect(reverse('my_bookings'))
        else:
            messages.error(
                request,
                'An error occurred, please try again')
    else:
        form = BookingForm()

    template = 'bookings.html'
    context = {
        'form': form
    }

    return render(request, template, context)
