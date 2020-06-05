from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import class_period_weekdays, class_date_range, calculate_cod
from pendulum import date, period


def datetime_string_to_date_object(datetime_string):
    """Function to convert datetime strings to date objects."""
    # TODO: How can we process variations in the input's datetime formats?
    class_date = datetime_string.split(",")
    class_date_year = int(class_date[0])
    class_date_month = int(class_date[1])
    class_date_day = int(class_date[2])

    return date(class_date_year, class_date_month, class_date_day)


class ValidationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        meets_expectations = False

        prefix = request.data.get("prefix")
        number = request.data.get("number")
        section = request.data.get("section")
        term = request.data.get("term")
        year = request.data.get("year")
        name = request.data.get("name")

        number_of_forms = int(request.data.get("meeting_times-TOTAL_FORMS"))

        total_meeting_minutes = 0.0

        for number in range(number_of_forms):
            number = str(number)

            delivery_method = request.data.get(f"meeting_times-{number}-delivery_method")
            start_date = request.data.get(f"meeting_times-{number}-start_date")
            end_date = request.data.get(f"meeting_times-{number}-end_date")
            start_time = request.data.get(f"meeting_times-{number}-start_time")
            end_time = request.data.get(f"meeting_times-{number}-end_time")
            recurrence = request.data.get(f"meeting_times-{number}-recurrence")



            if delivery_method and start_date and end_date and start_time and end_time and recurrence:
                print(
                    f"\n\n\nMeeting Time {number}: {delivery_method} Start Date: {start_date} End Date: {end_date} Start Time: {start_time}, End Time: {end_time}, Recurrence: {recurrence}")

                # TODO: How do we get the term's holidays from Colleague?
                # example holidays
                independence_day = date(2020, 4, 7)
                fall_break = period(date(2020, 8, 20), date(2020, 8, 25))
                OFF_DAYS = {independence_day, *fall_break}

                start_date = datetime_string_to_date_object(start_date)
                end_date = datetime_string_to_date_object(end_date)
                period_weekdays = class_period_weekdays(start_date, end_date, off_days=OFF_DAYS)
                print(f"period_weekdays: {period_weekdays}")

                # TODO: Get contact hours for each course's meeting type (How are we doing that?)
                class_contact_hours = 2  # placeholder

                weekdays = recurrence.split("BYDAY=")
                weekdays = weekdays[1].strip()
                weekdays = weekdays.split(",")   # Split class_weekdays string into a list
                days = ("MO", "TU", "WE", "TH", "FR", "SA", "SU")
                class_weekdays = tuple(day in weekdays for day in days)

                print(f"class_weekdays: {class_weekdays}")

                # Calculate COD
                minutes_per_class = calculate_cod(
                    class_weekdays,
                    class_contact_hours,
                    period_weekdays
                )

                print(f"minutes_per_class: {minutes_per_class}")

                # Calculate actual start and end dates for the course
                class_start_date, class_end_date = class_date_range(
                    start_date,
                    end_date,
                    OFF_DAYS,
                    class_weekdays
                )
                print(f"class_start_date, class_end_date: {class_start_date} {class_end_date}")

                total_meeting_minutes = total_meeting_minutes + minutes_per_class

        print(f"total_meeting_minutes: {total_meeting_minutes}")

        # TODO: Form to be displayed?
        if meets_expectations:
            return Response("Everything is A-OK", status=status.HTTP_200_OK)

        return Response("Need to tweak meeting hours", status=status.HTTP_417_EXPECTATION_FAILED)

