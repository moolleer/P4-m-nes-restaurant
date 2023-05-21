from django.shortcuts import render, reverse, redirect
from django.views import generic, View

from django.contrib import messages
from .models import Booking
from .forms import BookingForm


class Home(generic.TemplateView):
    """Opens to landing page"""
    template_name = "index.html"


def add_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
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
