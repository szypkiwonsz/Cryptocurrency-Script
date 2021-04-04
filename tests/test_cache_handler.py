from datetime import datetime
from unittest.mock import patch

import pytest
from httmock import all_requests, HTTMock

from database_handler import Currency
from tests.conftest import api_content


@all_requests
def api_mock(url, request):
    return {'status_code': 200,
            'content': api_content}


@pytest.mark.cache_handler
class TestCacheHandler:

    def test_get_dates_between_as_list_of_strings(self, cache_handler):
        dates = cache_handler.get_dates_between_as_list_of_strings(
            datetime(2012, 1, 1), datetime(2012, 1, 3), '%Y-%m-%dT23:59:59Z')
        assert dates == ['2012-01-01T23:59:59Z', '2012-01-02T23:59:59Z', '2012-01-03T23:59:59Z']

    def test_currency_column_contains_all_values_true(self, cache_handler, database_with_data):
        dates = ['2011-01-01T00:00:00Z']
        assert cache_handler.currency_column_contains_all_values(dates, 'time_open', 'btc-bitcoin') is True

    def test_currency_column_contains_all_values_false(self, cache_handler, database_with_data):
        dates = ['2011-01-01T00:00:00Z', '2011-01-04T00:00:00Z']
        assert cache_handler.currency_column_contains_all_values(dates, 'time_open', 'btc-bitcoin') is False

    def test_currency_time_close_column_contains_required_values_true(self, cache_handler, database_with_data):
        assert cache_handler.currency_time_close_column_contains_required_values(
            datetime(2011, 1, 1), datetime(2011, 1, 1), 'btc-bitcoin') is True

    def test_currency_time_close_column_contains_required_values_false(self, cache_handler, database_with_data):
        assert cache_handler.currency_time_close_column_contains_required_values(
            datetime(2011, 1, 1), datetime(2011, 1, 5), 'btc-bitcoin') is False

    def test_load_data_into_database_if_needed(self, cache_handler, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                cache_handler.load_data_into_database_if_needed(
                    datetime(2012, 2, 1), datetime(2012, 2, 3), 'btc-bitcoin')
                assert Currency.select().dicts()[-1]['time_open'] == '2012-02-03T00:00:00Z'
