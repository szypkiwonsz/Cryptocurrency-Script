import pytest
from peewee import SqliteDatabase

from cache_handler import CacheHandler
from data_loader import DataLoader
from database_handler import DatabaseHandler, Currency
from query_handler import QueryHandler, DateHandler, PriceHandler


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
        {'name': 'btc-bitcoin', 'time_open': '2011-01-02T00:00:00Z', 'time_close': '2011-01-02T23:59:59Z', 'open': 0.5,
         'high': 0.5, 'low': 0.5, 'close': 0.5},
        {'name': 'btc-bitcoin', 'time_open': '2011-01-03T00:00:00Z', 'time_close': '2011-01-03T23:59:59Z', 'open': 0.7,
         'high': 0.7, 'low': 0.7, 'close': 0.7},
        {'name': 'usdt-tether', 'time_open': '2011-01-01T00:00:00Z', 'time_close': '2011-01-01T23:59:59Z', 'open': 0.3,
         'high': 0.3, 'low': 0.3, 'close': 0.4, 'volume': 1245100000, 'market_cap': 38227791402}
    ]
    return currencies_data


@pytest.fixture()
def data_loader():
    data_loader = DataLoader()
    return data_loader


api_content = [
    {"time_open": "2012-02-01T00:00:00Z", "time_close": "2012-02-01T23:59:59Z", "open": 5.48, "high": 5.48,
     "low": 5.48, "close": 5.48},
    {"time_open": "2012-02-02T00:00:00Z", "time_close": "2012-02-02T23:59:59Z", "open": 6.08, "high": 6.08,
     "low": 6.08, "close": 6.08},
    {"time_open": "2012-02-03T00:00:00Z", "time_close": "2012-02-03T23:59:59Z", "open": 6.1, "high": 6.1,
     "low": 6.1, "close": 6.1}
]


@pytest.fixture()
def cache_handler():
    cache_handler = CacheHandler()
    return cache_handler


@pytest.fixture()
def database_with_data(database_handler, currencies_data):
    database_handler.insert_data_into_currency(currencies_data)
    return database_handler


@pytest.fixture()
def query_handler():
    query_handler = QueryHandler()
    return query_handler


@pytest.fixture()
def date_handler():
    date_handler = DateHandler()
    return date_handler


@pytest.fixture()
def price_handler():
    price_handler = PriceHandler()
    return price_handler
