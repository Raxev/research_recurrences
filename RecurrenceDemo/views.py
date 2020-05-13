from django.db import transaction
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DetailView, FormView

# from RecurrenceDemo.forms import MeetingTimeFormSet
from RecurrenceDemo.forms import MeetingTimeForm, MeetingTimeFormSet, CourseForm
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
    model = Course
    form_class = MeetingTimeForm
    pk_url_kwarg = "id"


"""
 Followed this article:
     https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6

 Even MORE information which inspired the first article can be found here:
    https://medium.com/@adandan01/django-inline-formsets-example-mybook-420cc4b6225d
    
 Uses Django Crispy Forms and Django dynamic formset jQuery plugin
    https://github.com/elo80ka/django-dynamic-formset
 To look like this:
     https://res.cloudinary.com/practicaldev/image/fetch/s--zCtBMru1--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://thepracticaldev.s3.amazonaws.com/i/olhglncci00mhx9w508t.png
"""


class CourseUpdate(UpdateView):
    model = Course
    template_name = "RecurrenceDemo/form.html"
    form_class = CourseForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["meeting_times"] = MeetingTimeFormSet(self.request.POST, instance=self.object)
        else:
            data["meeting_times"] = MeetingTimeFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        meeting_times = context["meeting_times"]
        self.object = form.save()
        if meeting_times.is_valid():
            meeting_times.instance = self.object
            meeting_times.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("RecurrenceDemo:detail", kwargs={"pk": self.object.pk})

    # def get_form(self, form_class=None):
    # FormSet = modelformset_factory(Course, exclude=("id", ))
    # course = Course.objects.get(id=self.kwargs.get("id"))
    # formset = FormSet(instance=course)
    # return formset
