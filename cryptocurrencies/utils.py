import calendar
from datetime import datetime


def date_with_last_day_of_month(date):
    """
    Changes date to date on the last day of the month.
    :param date: <datetime.datetime> -> datetime object
    :return: <datetime.datetime> -> datetime object with last day of the month
    """
    return datetime(date.year, date.month, calendar.monthrange(date.year, date.month)[1])


def file_with_extension(file_name, extension):
    if file_name.split('.')[-1] != extension:
        return f'{file_name}.{extension}'
    return file_name
