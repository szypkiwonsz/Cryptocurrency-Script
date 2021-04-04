from datetime import timedelta

import pandas as pd

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

    def get_currency_column_by_name(self, currency_name, column_name):
        """
        Gets list with values selected by database column and currency name.
        :param currency_name: <str> -> currency name
        :param column_name: <str> -> database column name
        :return: <list> -> list of values from selected column
        """
        currencies = self.get_all_currencies_by_name(currency_name).dicts()
        return [currency[column_name] for currency in currencies]


class DateHandler(QueryHandler):
    """Class storing methods to select currencies between two dates by name."""

    def get_all_currencies_by_name_between_dates(self, start_date, end_date, currency_name):
        """
        Gets all currencies data by name between dates from the database.
        :param start_date: <datetime.datetime> -> start date
        :param end_date: <datetime.datetime> -> end date
        :param currency_name: <str> -> currency name
        :return: <peewee.ModelSelect> -> class with currencies data by name between provided dates
        """
        return self.get_all_currencies_by_name(currency_name).where(Currency.time_close.between(
            start_date, end_date + timedelta(days=1)))


class PriceHandler(DateHandler):
    """Inheriting class storing methods to get selected currency price data by days between two dates."""

    @staticmethod
    def get_currencies_prices_by_day(currencies):
        """
        Gets pandas DataFrame with currency prices by days.
        :param currencies: <peewee.ModelSelect> -> class with currency data
        :return: <pandas.core.frame.DataFrame> -> pandas DataFrame with currency prices by days
        """
        pd.set_option('display.max_rows', None)  # setting for no limit of displayed data
        df = pd.DataFrame({
            'name': [currency['name'] for currency in currencies],
            'date': [currency['time_close'] for currency in currencies],
            'price': [currency['close'] for currency in currencies]}
        )
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_currency_price_by_day_between_dates(self, start_date, end_date, currency_name):
        """
        Gets pandas DataFrame with selected currency prices data by days between two dates.
        :param start_date: <datetime.datetime> -> start date
        :param end_date: <datetime.datetime> -> end date
        :param currency_name: <str> -> currency name
        :return: <pandas.core.frame.DataFrame> -> pandas DataFrame with currency prices by days between two dates
        """
        currencies = self.get_all_currencies_by_name_between_dates(start_date, end_date, currency_name).dicts()
        return self.get_currencies_prices_by_day(currencies)


class AveragePriceHandler(PriceHandler):
    """Inheriting class storing methods to get selected currency average price by months between two dates."""

    @staticmethod
    def calculate_average_price_by_month(df):
        """
        Calculates average price of currency by month.
        :param df: <pandas.core.frame.DataFrame> -> pandas DataFrame with currency prices
        :return: <pandas.core.frame.DataFrame> -> pandas DataFrame with the calculated average currency price
        """
        df = df.groupby([df['date'].dt.year.rename('year'), df['date'].dt.month.rename('month')]).mean().round(2)
        df.rename(columns={'price': 'average price ($)'}, inplace=True)
        return df

    def get_average_price_by_month_from_time_period(self, start_date, end_date, currency_name):
        """
        Gets average price of currency by month for given period.
        :param start_date: <datetime.datetime> -> start date
        :param end_date: <datetime.datetime> -> end date
        :param currency_name: <str> -> currency name
        :return: <pandas.core.frame.DataFrame> -> pandas DataFrame with the calculated average currency price
        """
        currency_prices = self.get_currency_price_by_day_between_dates(start_date, end_date, currency_name)
        return self.calculate_average_price_by_month(currency_prices)
