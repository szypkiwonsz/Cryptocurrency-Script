from datetime import datetime

import pytest
from httmock import HTTMock, all_requests

from cryptocurrencies.tests.conftest import api_content


@all_requests
def api_mock(url, request):
    return {'status_code': 200,
            'content': api_content}


@pytest.mark.data_loader
class TestDataLoader:

    def test_load_data_from_api(self, data_loader):
        with HTTMock(api_mock):
            data_loader.load_data_from_api(datetime(2012, 2, 1), datetime(2012, 2, 3), 'btc-bitcoin')
            assert data_loader.data == api_content

    def test_update_dictionary_with_name(self, data_loader):
        empty_dict = {}
        data_loader.update_dictionary_with_name(empty_dict, 'btc-bitcoin')
        assert empty_dict['name'] == 'btc-bitcoin'

    def test_modify_data(self, data_loader):
        data_loader.data = api_content
        data_loader.modify_data('btc-bitcoin')
        assert data_loader.data[0]['name'] == 'btc-bitcoin'
