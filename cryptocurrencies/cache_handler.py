import pandas as pd

from data_loader import DataLoader
from database_handler import DatabaseHandler
from query_handler import QueryHandler


class CacheHandler:
    """A class dealing with checking whether the required data is in the database, otherwise it gets it from the API."""

    @staticmethod
    def get_dates_between_as_list_of_strings(start_date, end_date, date_format):
        """
        Gets dates between two dates as a list of strings in the selected format.
        :param start_date: <datetime.datetime> -> start date
        :param end_date: <datetime.datetime> -> end date
        :param date_format: <str> -> format of the date to get
        :return: <list> -> list of dates as strings
        """
        return list(pd.date_range(start_date, end_date).strftime(date_format))

    def database_contains_all_data(self, start_date, end_date, currency_name):
        """
        Compares whether dates between arguments are contained in the data for a particular currency in the database.
        :param start_date: <datetime.datetime> -> start date of the required data
        :param end_date: <datetime.datetime> -> end date of the required data
        :param currency_name: <str> -> currency name
        :return: <bool> -> True if the data contains all the dates for a particular currency, False if not
        """
        temp_query_handler = QueryHandler()
        dates_between_arguments = self.get_dates_between_as_list_of_strings(start_date, end_date, '%Y-%m-%dT23:59:59Z')
        currency_dates_in_database = temp_query_handler.get_currencies_column_by_name_between_dates(
            start_date, end_date, currency_name, 'time_close')
        return set(dates_between_arguments).issubset(currency_dates_in_database)

    def load_data_into_database_if_needed(self, start_date, end_date, currency_name):
        """
        Gets, modifies and enters data from the API if the required data is not in the database.
        :param start_date: <datetime.datetime> -> start date of the required data
        :param end_date: <datetime.datetime> -> end date of the required data
        :param currency_name: <str> -> currency name
        """
        # initialization before checking the contents of the database due to the possibility of no database created
        temp_database_handler = DatabaseHandler()
        if not self.database_contains_all_data(start_date, end_date, currency_name):
            temp_json_loader = DataLoader()
            temp_json_loader.load_data_from_api(start_date, end_date, currency_name)
            temp_json_loader.modify_data(currency_name)
            temp_database_handler.insert_data_into_currency(temp_json_loader.data)
