from django import forms
from django.contrib.auth.forms import UserCreationForm
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
        widgets = {'time': forms.Select(
            choices=BOOKING_TIMES), 'no_of_guests': forms.Select(
                choices=NO_OF_GUESTS_CHOICE), 'date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}),
                'message': forms.Textarea(attrs={
                    'placeholder': 'Write your message here..'})}


# class NewUserForm(UserCreationForm):
#     """Sign up form"""
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")

#     def save(self, commit=True):
#         user = super(NewUserForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user
