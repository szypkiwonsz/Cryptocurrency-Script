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
