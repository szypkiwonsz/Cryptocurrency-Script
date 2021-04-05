from datetime import datetime

import pytest


@pytest.mark.query_handler
class TestQueryHandler:

    def test_get_all_currencies(self, query_handler, database_with_data):
        assert query_handler.get_all_currencies().count() == 4

    def test_get_all_currencies_by_name(self, query_handler, database_with_data):
        assert query_handler.get_all_currencies_by_name('btc-bitcoin').count() == 3

    def test_get_currency_column_by_name(self, query_handler, database_with_data):
        assert query_handler.get_currency_column_by_name('btc-bitcoin', 'close')[0] == 0.3


@pytest.mark.date_handler
class TestDateHandler:

    def test_get_all_currencies_by_name_between_dates(self, date_handler, database_with_data):
        assert date_handler.get_all_currencies_by_name_between_dates(
            datetime(2011, 1, 1), datetime(2011, 1, 3), 'btc-bitcoin').dicts()[-1]['close'] == 0.7


@pytest.mark.price_handler
class TestPriceHandler:

    def test_get_currencies_prices_by_day(self, price_handler, query_handler, database_with_data):
        currencies = query_handler.get_all_currencies_by_name('btc-bitcoin').dicts()
        price_list = price_handler.get_currencies_prices_by_day(currencies)
        assert price_list.to_dict('records')[0]['price'] == 0.3

    def test_get_currency_price_by_day_between_dates(self, price_handler, database_with_data):
        price_list = price_handler.get_currency_price_by_day_between_dates(
            datetime(2011, 1, 1), datetime(2011, 1, 2), 'usdt-tether')
        assert price_list.to_dict('records')[0]['price'] == 0.4


@pytest.mark.average_price_handler
class TestAveragePriceHandler:

    def test_calculate_average_price_by_month(self, average_price_handler, price_handler, database_with_data):
        price_list = price_handler.get_currency_price_by_day_between_dates(
            datetime(2011, 1, 1), datetime(2011, 1, 3), 'btc-bitcoin')
        average_price = average_price_handler.calculate_average_price_by_month(price_list)
        assert average_price.to_dict('records')[0]['average price ($)'] == 0.5

    def test_get_average_price_by_month_from_time_period(self, average_price_handler, database_with_data):
        average_price = average_price_handler.get_average_price_by_month_from_time_period(
            datetime(2011, 1, 1), datetime(2011, 1, 3), 'btc-bitcoin')
        assert average_price.to_dict('records')[0]['average price ($)'] == 0.5


@pytest.mark.consecutive_price_increase_handler
class TestConsecutivePriceIncreaseHandler:

    def test_calculate_consecutive_price_increases(self, consecutive_price_increase_handler, price_handler,
                                                   database_with_data):
        price_list = price_handler.get_currency_price_by_day_between_dates(
            datetime(2011, 1, 1), datetime(2011, 1, 3), 'btc-bitcoin')
        price_increases = consecutive_price_increase_handler.calculate_consecutive_price_increases(price_list)
        assert price_increases.to_dict('records')[0][('price', 'sum')] == 1.5

    def test_get_consecutive_price_increases_period(self, consecutive_price_increase_handler, database_with_data):
        price_increases = consecutive_price_increase_handler.get_consecutive_price_increases_period(
            datetime(2011, 1, 1), datetime(2011, 1, 3), 'btc-bitcoin')
        assert price_increases.to_dict('records')[0][('price', 'sum')] == 1.5

    def test_get_longest_consecutive_price_increases_period(self, consecutive_price_increase_handler,
                                                            database_with_data):
        longest_increases = consecutive_price_increase_handler.get_longest_consecutive_price_increases_period(
            datetime(2011, 1, 1), datetime(2011, 1, 3), 'btc-bitcoin')
        assert longest_increases.to_dict('records')[0][('price', 'sum')] == 1.5

    def test_get_longest_consecutive_price_increase_as_msg(self, consecutive_price_increase_handler,
                                                           database_with_data):
        longest_increases_records = consecutive_price_increase_handler.get_longest_consecutive_price_increases_period(
            datetime(2011, 1, 1), datetime(2011, 1, 3), 'btc-bitcoin').to_dict('records')
        longest_increase_record = longest_increases_records[0]
        longest_increase_msg = consecutive_price_increase_handler.get_longest_consecutive_price_increase_as_msg(
            longest_increase_record)
        assert longest_increase_msg == ('Longest consecutive period was from 2011-01-01 to 2011-01-03 with increase '
                                        'of $1.5')
