from django import forms
from .models import Booking
import datetime as dt

BOOKING_TIMES = [(
    dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(16, 22)]

NO_OF_GUESTS_CHOICE = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
]


class BookingForm(forms.ModelForm):
    """Booking Form"""

    class Meta:
        model = Booking
        fields = ['date', 'time', 'no_of_guests', 'message']
        widgets = {'time': forms.Select(choices=BOOKING_TIMES)}
        widgets = {'no_of_guests': forms.Select(choices=NO_OF_GUESTS_CHOICE)}
