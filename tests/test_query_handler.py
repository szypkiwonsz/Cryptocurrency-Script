import pytest


@pytest.mark.query_handler
class TestQueryHandler:

    def test_get_all_currencies(self, query_handler, database_with_data):
        assert query_handler.get_all_currencies().count() == 2

    def test_get_all_currencies_by_name(self, query_handler, database_with_data):
        assert query_handler.get_all_currencies_by_name('btc-bitcoin').count() == 1

    def test_get_currency_column_by_name(self, query_handler, database_with_data):
        assert query_handler.get_currency_column_by_name('btc-bitcoin', 'close')[0] == 0.3
