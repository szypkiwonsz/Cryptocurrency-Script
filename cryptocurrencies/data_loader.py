from datetime import timedelta

from coinpaprika import client as Coinpaprika


class DataLoader:
    """Class that loads and modifies data stored in list of json objects."""

    def __init__(self):
        self.data = []

    def load_data_from_api(self, start_date, end_date, currency_name):
        """Loads a specific data about currencies from a given time period from api.
        :param start_date: <datetime.datetime> -> start date of the required data
        :param end_date: <datetime.datetime> -> end date of the required data
        :param currency_name: <str> -> currency name
        """
        client = Coinpaprika.Client()
        while start_date <= end_date:
            self.data += client.candles(currency_name, start=start_date.date(), end=end_date.date())
            # the start_date must be increased by 365 days due to the error with not uploading one day from a leap year
            start_date += timedelta(days=365)

    @staticmethod
    def update_dictionary_with_name(dictionary, currency_name):
        """
        Updates existing dictionary containing data about currency with a new dictionary with currency name.
        :param dictionary: <dict> -> dictionary with data about currency
        :param currency_name: <str> -> currency name
        :return: <dict> -> updated dictionary which includes currency name
        """
        return dictionary.update({'name': currency_name})

    def modify_data(self, currency_name):
        """
        Modifies the elements of data needed for the correct operation of the program.
        :param currency_name: <str> -> currency name
        """
        for element in self.data:
            self.update_dictionary_with_name(element, currency_name)