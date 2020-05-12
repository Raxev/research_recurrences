from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DetailView, FormView

# from RecurrenceDemo.forms import MeetingTimeFormSet
from RecurrenceDemo.forms import MeetingTimeUpdateForm
from RecurrenceDemo.models import Course, MeetingTime


class CourseList(ListView):
    model = Course
    template_name = "RecurrenceDemo/course_list.html"
    context_object_name = "courses"


class DemoDetailView(DetailView):
    template_name = "RecurrenceDemo/detail.html"
    success_url = reverse_lazy("RecurrenceDemo:course_list")
    model = Course
    pk_url_kwarg = "id"


class DemoUpdateView(UpdateView):
    template_name = "RecurrenceDemo/update.html"
    success_url = reverse_lazy("RecurrenceDemo:course_list")
    model = MeetingTime
    form_class = MeetingTimeUpdateForm
    pk_url_kwarg = "id"


class DemoFormView(FormView):
    form_class = modelformset_factory(Course, exclude=("id", ))
    template_name = "RecurrenceDemo/form.html"




    # def get_form(self, form_class=None):
        # FormSet = modelformset_factory(Course, exclude=("id", ))
        # course = Course.objects.get(id=self.kwargs.get("id"))
        # formset = FormSet(instance=course)
        # return formset


