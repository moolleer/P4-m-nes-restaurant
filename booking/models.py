from django.db import models
import uuid
from django.contrib.auth.models import User


class Table(models.Model):
    table_number = models.IntegerField()
    max_no_guests = models.IntegerField()

    def __str__(self):
        return f'Table {self.table_number}, max guests {self.max_no_guests}'


class Booking(models.Model):
    booking_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    booked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bookings")
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    no_of_guests = models.IntegerField()
    message = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'Booking {self.date}, {self.time} by {self.booked_by}'
