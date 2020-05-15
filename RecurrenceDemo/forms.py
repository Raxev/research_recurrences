from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
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
    fields="__all__",
    extra=5,
    max_num=10,
    can_delete=True
)


class CourseForm(forms.ModelForm):
    class Meta:
        """Meta. class."""

        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('prefix'),
                Field('number'),
                Field('section'),
                Field('term'),
                Field('year'),
                Field('name'),
                Fieldset('Add meeting times',
                         Formset('meeting_times')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'submit')),
            )
        )

# https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/#inline-formsets
