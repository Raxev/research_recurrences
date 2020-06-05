from typing import Tuple, Iterable, TYPE_CHECKING

from pendulum import date, period

if TYPE_CHECKING:
    from pendulum import Date

BREAK_NEEDED_PER_X_MINUTES = 90
MINUTES_PER_BREAK = 10
REQUIRED_MINUTES_PER_CREDIT_HOUR = 800


def class_period_weekdays(start_date: 'Date',
                          end_date: 'Date',
                          off_days: Iterable['Date']) -> Tuple[int, ...]:
    """
    Calculates the number of days each week day occurs in a given period
    aside from holidays

    :param start_date: The inclusive start date of the class period.
    :param end_date: The inclusive end date of the class period.
    :param off_days: The dates of all holidays in the class period.
        May contain holidays outside of the class period.
    :return: A tuple where the index represents the weekday and the value
        represents the number of class days for this weekday in the given
        class period. Monday is at index 0 and Sunday is at 6.

    >>> mlk = date(2020, 1, 20)
    >>> spring_break = period(date(2020, 3, 9), date(2020, 3, 15))
    >>> spring_holidays = period(date(2020, 4, 10), date(2020, 4, 12))
    >>> OFF_DAYS = {mlk, *spring_break, *spring_holidays}
    >>> class_period_weekdays(
    ...     start_date=date(2020, 1, 13),
    ...     end_date=date(2020, 5, 12),
    ...     off_days=OFF_DAYS)
    (16, 17, 16, 16, 15, 15, 15)
    """

    off_days = set(off_days)
    class_weekdays = [0] * 7

    for day in period(start_date, end_date):
        if day not in off_days:
            class_weekdays[day.weekday()] += 1

    return tuple(class_weekdays)


def class_date_range(start_date: 'Date',
                     end_date: 'Date',
                     off_days: Iterable['Date'],
                     class_weekdays: Tuple[bool, bool, bool, bool, bool, bool, bool]) -> Tuple['Date', 'Date']:
    """
    Calculates the start and end dates for a class.

    :param start_date: The inclusive start date of the class period.
    :param end_date: The inclusive end date of the class period.
    :param off_days: The dates of all holidays in the class period.
        May contain holidays outside of the class period.
    :param class_weekdays: What days will the class meet?
        Monday is at index 0 and Sunday is at 6.
    :return: The start and end date for a class that meets the given weekdays in the period.

    >>> mlk = date(2020, 1, 20)
    >>> spring_break = period(date(2020, 3, 9), date(2020, 3, 15))
    >>> spring_holidays = period(date(2020, 4, 10), date(2020, 4, 12))
    >>> off_days = {mlk, *spring_break, *spring_holidays}
    >>> start_and_end = class_date_range(
    ...     start_date=date(2020, 1, 13),
    ...     end_date=date(2020, 5, 12),
    ...     off_days=off_days,
    ...     class_weekdays=(True, False, True, False, False, False, False))
    >>> print(start_and_end)
    (Date(2020, 1, 13), Date(2020, 5, 11))
    """

    class_start_date = None
    class_end_date = None
    off_days = set(off_days)

    for day in period(start_date, end_date):

        if day in off_days:
            continue

        if class_weekdays[day.weekday()]:
            class_start_date = day
            break

    for day in reversed([*period(start_date, end_date)]):

        if day in off_days:
            continue

        if class_weekdays[day.weekday()]:
            class_end_date = day
            break

    return class_start_date, class_end_date


def calculate_cod(
        class_weekdays: Tuple[bool, bool, bool, bool, bool, bool, bool],
        class_credit_hours: int,
        class_period_weekdays: Tuple[int, int, int, int, int, int, int]) -> float:
    """

    :param class_weekdays: What days will the class meet?
        Monday is at index 0 and Sunday is at 6.
    :param class_credit_hours: How many credit hours does the class have?
    :param class_period_weekdays: A tuple where the index represents the weekday and
        the value represents the number of class days for this weekday in the given
        class period. Monday is at index 0 and Sunday is at 6.
    :return: The minimum number of minutes each class needs to last. It's recommended
        to round up to a multiple of 5.

    >>> calculate_cod(
    ...    class_weekdays=(True, False, True, False, False, False, False),
    ...    class_credit_hours=3,
    ...    class_period_weekdays=(16, 17, 16, 16, 15, 15, 15))
    75.0
    """

    if not any(class_weekdays):
        raise ValueError("At least one week day must be checked.")

    # Remember that booleans (x) are worth 0 or 1. So we're adding up all the days where
    # the class will meet.

    class_weekday_count = sum(x * y for x, y in zip(class_weekdays, class_period_weekdays))

    class_needed_minutes = class_credit_hours * REQUIRED_MINUTES_PER_CREDIT_HOUR

    minutes_per_class_minus_breaks = class_needed_minutes / class_weekday_count

    needed_breaks = minutes_per_class_minus_breaks // BREAK_NEEDED_PER_X_MINUTES

    minutes_per_class = minutes_per_class_minus_breaks + needed_breaks * MINUTES_PER_BREAK

    return minutes_per_class
