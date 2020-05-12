from django.contrib import admin

# Register your models here.
from RecurrenceDemo import models


def get_fields(model, exclude=None):
    fields = []

    if isinstance(exclude, str):
        exclude = [exclude]

    for field in model._meta.fields:
        if exclude and field.name in exclude:
            continue
        fields.append(field.name)
    return fields


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = get_fields(models.Course)
    search_fields = get_fields(models.Course)


@admin.register(models.MeetingTime)
class MeetingTimeAdmin(admin.ModelAdmin):
    list_display = get_fields(models.MeetingTime)
    search_fields = get_fields(models.MeetingTime)


