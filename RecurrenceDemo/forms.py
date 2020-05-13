from django import forms
from django.forms import inlineformset_factory

from RecurrenceDemo.models import MeetingTime, Course


class MeetingTimeForm(forms.ModelForm):
    class Meta:
        """Meta class."""

        model = MeetingTime
        exclude = ()

    class Media:
        js = ('recurrence/js/recurrence.js',
              'recurrence/js/recurrence-widget.js')
        css = {
            'all': ('recurrence/css/recurrence.css',)
        }


MeetingTimeFormSet = inlineformset_factory(
    Course, MeetingTime,
    form=MeetingTimeForm,
    fields=["type", "start", "end", "recurrence", "course"],
    extra=2,
    can_delete=True
)


class CourseForm(forms.ModelForm):
    class Meta:
        """Meta. class."""

        model = Course
        fields = "__all__"



# https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/#inline-formsets
