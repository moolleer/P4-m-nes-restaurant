from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    """Booking Form"""

    class Meta:
        model = Booking
        fields = ['date', 'time', 'no_of_guests', 'message']
