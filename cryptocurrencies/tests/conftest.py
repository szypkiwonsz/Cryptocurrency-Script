import pytest
from peewee import SqliteDatabase

from cryptocurrencies.database_handler import DatabaseHandler, Currency


# fixtures for database_handler.py file
@pytest.fixture()
def database():
    test_db = SqliteDatabase(':memory:')
    test_db.bind([Currency], bind_refs=False, bind_backrefs=False)
    return test_db


@pytest.fixture()
def database_handler(database):
    database_handler = DatabaseHandler()
    database_handler.db = database
    return database_handler


@pytest.fixture()
def currencies_data():
    currencies_data = [
        {'name': 'btc-bitcoin', 'time_open': '2011-01-01T00:00:00Z', 'time_close': '2011-01-01T23:59:59Z', 'open': 0.3,
         'high': 0.3, 'low': 0.3, 'close': 0.3},
        {'name': 'usdt-tether', 'time_open': '2011-01-01T00:00:00Z', 'time_close': '2011-01-01T23:59:59Z', 'open': 0.3,
         'high': 0.3, 'low': 0.3, 'close': 0.4, 'volume': 1245100000, 'market_cap': 38227791402}
    ]
    return currencies_data
