from django.db import models
from django.db.models import ForeignKey

from recurrence.fields import RecurrenceField

# Create your models here.


class Course(models.Model):
    prefix = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    term = models.CharField(max_length=3)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.prefix} {self.number}-{self.section} {self.term}{self.year}"


# MeetingInformation
class MeetingTime(models.Model):
    """Models a meeting time."""
    delivery_method = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    recurrence = RecurrenceField(blank=True)
    course = ForeignKey(to=Course, related_name="meeting_times", on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation."""
        return f"{self.delivery_method} {self.start_date} {self.end_date}. {self.start_time} - {self.end_time}. {self.recurrence}"

