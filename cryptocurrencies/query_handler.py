from datetime import timedelta

from database_handler import Currency


class QueryHandler:
    """Class storing methods for basics database queries."""

    @staticmethod
    def get_all_currencies():
        """
        Gets all currencies data from the database.
        :return: <peewee.ModelSelect> -> class with currencies data
        """
        return Currency.select()

    def get_all_currencies_by_name(self, currency_name):
        """
        Gets all currencies data by name from the database.
        :param currency_name: <str> -> currency name
        :return: <peewee.ModelSelect> -> class with currencies data by name
        """
        return self.get_all_currencies().where(Currency.name == currency_name)

    def get_all_currencies_by_name_between_dates(self, start_date, end_date, currency_name):
        """
        Gets all currencies data by name between dates from the database.
        :param start_date: <datetime.datetime> -> start date of the searched data
        :param end_date: <datetime.datetime> -> end date of the searched data
        :param currency_name: <str> -> currency name
        :return: <peewee.ModelSelect> -> class with currencies data by name between provided dates
        """
        return self.get_all_currencies_by_name(currency_name).where(Currency.time_close.between(
            start_date, end_date + timedelta(days=1)))

    def get_currency_column_by_name(self, currency_name, column_name):
        """
        Gets list with values selected by database column and currency name.
        :param currency_name: <str> -> currency name
        :param column_name: <str> -> database column name
        :return: <list> -> list of values from selected column
        """
        currencies = self.get_all_currencies_by_name(currency_name).dicts()
        return [currency[column_name] for currency in currencies]
