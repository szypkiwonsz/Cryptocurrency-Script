import pytest

from database_handler import Currency


@pytest.mark.database_handler
class TestDatabaseHandler:

    def test_create_table(self, database_handler):
        database_handler.create_table(Currency)
        assert database_handler.db.get_tables()[0] == 'currency'

    def test_insert_data_into_currency(self, database_handler, currencies_data):
        database_handler.insert_data_into_currency(currencies_data)
        assert Currency.select().dicts()[0]['name'] == 'btc-bitcoin'
        assert Currency.select().dicts()[3]['name'] == 'usdt-tether'
        assert Currency.select().dicts()[0]['volume'] is None
        assert Currency.select().dicts()[3]['volume'] == 1245100000

    def test_insert_data(self, database_handler, currencies_data):
        database_handler.insert_data(currencies_data, Currency)
        assert Currency.select().dicts()[0]['close'] == 0.3
        assert Currency.select().dicts()[3]['close'] == 0.4
        assert Currency.select().dicts()[0]['market_cap'] is None
        assert Currency.select().dicts()[3]['market_cap'] == 38227791402


@pytest.mark.database_handler
class TestCurrencyModel:

    def test_uniqueness(self, database_handler, currencies_data):
        database_handler.insert_data_into_currency(currencies_data)
        database_handler.insert_data_into_currency(currencies_data)
        assert Currency.select().count() == 4

    def test_uniqueness_same_dates_different_names(self, database_handler, currencies_data):
        database_handler.insert_data_into_currency(currencies_data)
        assert Currency.select().count() == 4

    def test_uniqueness_same_dates_same_names(self, database_handler, currencies_data):
        currencies_data[3]['name'] = 'btc-bitcoin'
        database_handler.insert_data_into_currency(currencies_data)
        assert Currency.select().count() == 3
