from django import forms
from django.forms import modelformset_factory

from RecurrenceDemo.models import MeetingTime, Course


class MeetingTimeUpdateForm(forms.ModelForm):

    class Meta:
        """Meta class."""

        model = MeetingTime
        fields = ["type", "start", "end", "recurrence", "course"]

    class Media:
        js = ('recurrence/js/recurrence.js',
              'recurrence/js/recurrence-widget.js')
        css = {
            'all': ('recurrence/css/recurrence.css',)
        }


# MeetingTimeFormSet = modelformset_factory(MeetingTime, fields=("type", "start", "end", "recurrence", "course"))


class CourseForm(forms.ModelForm):

    class Meta:
        """Meta. class."""

        model = Course
        fields = "__all__"
