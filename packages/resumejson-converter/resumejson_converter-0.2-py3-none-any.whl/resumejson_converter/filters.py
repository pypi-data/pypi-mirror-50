from datetime import datetime
from babel.dates import format_date

import resumejson_converter.utils.templates as utemplates


def dateedit(startDate, endDate):
    """
    Return the date in special format.

    If only the start date is specified: 2019 - Auj.

    >>> dateedit("2019-01-01", "")
    "2019 - Auj."

    Else if the year of the start date and the year of the end data are the
    same: 2019

    >>> dateedit("2019-01-01", "2019-02-02")
    "2019"

    Else if the year of start date are not the same that the year of the end
    date: 2017 - 2019

    >>> datetime("2019-01-01", "2017-05-01")
    "2019 - 2017"
    """
    startDateTime = datetime.strptime(startDate, '%Y-%m-%d')
    if endDate == "":
        return "{:%Y} - Auj.".format(startDateTime)
    else:
        endDateTime = datetime.strptime(endDate, '%Y-%m-%d')
        diffDate = endDateTime - startDateTime
        if startDateTime.strftime("%Y") == endDateTime.strftime("%Y"):
            return "{:%Y}".format(startDateTime)
        else:
            return "{:%Y} - {:%Y}".format(startDateTime, endDateTime)


def datediff(title, startDate, endDate, showDiff=True):
    """
    Return time passed between two dates after a text.

    >>> datediff("Hello World", "2019-01-02", "2019-06-02")
    'Hello World - 5 mois'
    """
    if showDiff and endDate != "":
        startDateTime = datetime.strptime(startDate, '%Y-%m-%d')
        endDateTime = datetime.strptime(endDate, '%Y-%m-%d')
        diffDate = endDateTime - startDateTime
        period = utemplates.td_format(diffDate).split(',')[0]
        return "{} - {}".format(title, period)
    else:
        return "{}".format(title)


def birthday(date):
    """
    Return a date in french format.

    >>> birthday("1990-10-25")
    '25 octobre 1990'
    """
    date = datetime.strptime(date, '%Y-%m-%d')
    return format_date(date, format='long', locale='fr')


def clean(phone):
    """
    Return phone number in french format.

    >>> clean("0011223344")
    '00 11 22 33 44'
    """
    phone = [phone[num:num+2] for num in range(0, len(phone), 2)]
    return " ".join(phone)
