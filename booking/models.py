from django.db import models
import uuid
from django.contrib.auth.models import User
import datetime as dt


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
    time = models.TimeField(default=dt.time(00, 00))
    no_of_guests = models.IntegerField()
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="table", null=True)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'Booking {self.date}, {self.time} by {self.booked_by}'

    def assign_table(self):
        if self.date and self.time:
            # Retrieve available tables for the booking's date and time
            available_tables = Table.objects.filter(
                max_no_guests__gte=self.no_of_guests
            ).exclude(
                table__date=self.date,
                table__time=self.time
            ).order_by('max_no_guests')

            if available_tables:
                self.table = available_tables.first()
                self.save()
                return True
        self.table = None
        return False

    def save(self, *args, **kwargs):
        if not self.pk:
            # If its a new booking, assign a table
            self.assign_table()
        super().save(*args, **kwargs)


# class User(models.Model):
#     username = models.CharField(null=False)
#     email = models.EmailField(null=False)
#     password = models.CharField()
#     password2 = models.CharField()
