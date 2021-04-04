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

    @staticmethod
    def currency_column_contains_all_values(values, column_to_compare, currency_name):
        """
        Compares whether provided values are contained in the data for a particular currencies in a currency table
        column in the database.
        :param values: <list> -> list of values to compare
        :param column_to_compare: <str> -> database column name
        :param currency_name: <str> -> currency name
        :return: <bool> -> True if the values from database contains all the provided values, False if not
        """
        temp_query_handler = QueryHandler()
        currency_column_values = temp_query_handler.get_currency_column_by_name(currency_name, column_to_compare)
        return set(values).issubset(currency_column_values)

    def currency_time_close_column_contains_required_values(self, start_date, end_date, currency_name):
        """
        Compares whether dates between arguments are contained in the data for a particular currencies in a currency
        table 'time_close' column in the database.
        column in the database.
        :param start_date: <datetime.datetime> -> start date of the required data
        :param end_date: <datetime.datetime> -> end date of the required data
        :param currency_name: <str> -> currency name
        :return: <bool> -> True if the 'time_close' column values contains all dates between arguments, False if not
        """
        dates_between_arguments = self.get_dates_between_as_list_of_strings(start_date, end_date, '%Y-%m-%dT23:59:59Z')
        return self.currency_column_contains_all_values(dates_between_arguments, 'time_close', currency_name)

    def load_data_into_database_if_needed(self, start_date, end_date, currency_name):
        """
        Gets, modifies and enters data from the API if the required data is not in the database.
        :param start_date: <datetime.datetime> -> start date of the required data
        :param end_date: <datetime.datetime> -> end date of the required data
        :param currency_name: <str> -> currency name
        """
        # initialization before checking the contents of the database due to the possibility of no database created
        temp_database_handler = DatabaseHandler()
        if not self.currency_time_close_column_contains_required_values(start_date, end_date, currency_name):
            temp_json_loader = DataLoader()
            temp_json_loader.load_data_from_api(start_date, end_date, currency_name)
            temp_json_loader.modify_data(currency_name)
            temp_database_handler.insert_data_into_currency(temp_json_loader.data)
