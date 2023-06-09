# Generated by Django 3.2.19 on 2023-05-24 11:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField()),
                ('max_no_guests', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField(default=datetime.time(0, 0))),
                ('no_of_guests', models.IntegerField()),
                ('message', models.TextField(blank=True)),
                ('booked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bookings', to=settings.AUTH_USER_MODEL)),
                ('table', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='table', to='booking.table')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
