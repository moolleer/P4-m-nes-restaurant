from django.shortcuts import render, reverse, redirect
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
            booking_date = form.cleaned_data['date']
            booking_time = form.cleaned_data['time']
            print(booking_date)
            existing_bookings = Booking.objects.filter(
                date=booking_date, time=booking_time)
            for booking in existing_bookings:
                print(booking)
            if existing_bookings.exists():
                messages.error(
                    request, 'A booking already exists for this day and time.')
                print('booking exists')
            else:
                available_tables = check_available_tables(
                    booking_date, booking_time, form.cleaned_data[
                        'no_of_guests'])
                print(available_tables)
                print('Hej')
                if available_tables:
                    form.instance.booked_by = request.user
                    form.save()
                    messages.success(request, 'Booking completed')
                else:
                    messages.error(
                        request, 'No more available tables for this day and time.')
                    print('no more available tables')
            return redirect(reverse('bookings'))
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


# def tables(requested_date, requested_time, no_of_guests):
#     table_list = []
#     all_tables = Table.objects.all()
#     for table in all_tables:
#         if table.date :
#             table.booked = True
#         else:
#             table_list.append(table.table_number)
#     print(table_list)
#     return table_list


def check_available_tables(date, time, no_of_guests):
    available_tables = Table.objects.filter(
        booked=False, max_no_guests__gte=no_of_guests)

    for table in available_tables:
        print(table)
    return available_tables
