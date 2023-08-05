from datetime import datetime
from babel.dates import format_date

import resumejson_converter.utils.templates as utemplates


def dateedit(startDate, endDate):
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
    if showDiff and endDate != "":
        startDateTime = datetime.strptime(startDate, '%Y-%m-%d')
        endDateTime = datetime.strptime(endDate, '%Y-%m-%d')
        diffDate = endDateTime - startDateTime
        period = utemplates.td_format(diffDate).split(',')[0]
        return "{} - {}".format(title, period)
    else:
        return "{}".format(title)


def birthday(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return format_date(date, format='long', locale='fr')


def clean(phone):
    phone = [phone[num:num+2] for num in range(0, len(phone), 2)]
    return " ".join(phone)
