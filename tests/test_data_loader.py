from datetime import datetime

import click
import pytest
from coinpaprika.exceptions import CoinpaprikaAPIException
from httmock import HTTMock, all_requests, response

from tests.conftest import api_content


@all_requests
def api_mock(url, request):
    return {'status_code': 200,
            'content': api_content}


@all_requests
def api_mock_id_not_found(url, request):
    headers = {'content-type': 'application/json'}
    content = {'error': 'id not found'}
    return response(404, content, headers)


@all_requests
def api_mock_incorrect_parameters(url, request):
    headers = {'content-type': 'application/json'}
    content = {'error': 'incorrect parameters'}
    return response(400, content, headers)


@pytest.mark.data_loader
class TestDataLoader:

    def test_load_data_from_api(self, data_loader):
        with HTTMock(api_mock):
            data_loader.load_data_from_api(datetime(2012, 2, 1), datetime(2012, 2, 3), 'btc-bitcoin')
            assert data_loader.data == api_content

    def test_load_data_from_api_bad_coin_parameter(self, data_loader):
        with HTTMock(api_mock_id_not_found):
            with pytest.raises(click.BadParameter):
                data_loader.load_data_from_api(datetime(2012, 2, 1), datetime(2012, 2, 3), 'btc-bitco')

    def test_load_data_from_api_incorrect_parameters(self, data_loader):
        with HTTMock(api_mock_incorrect_parameters):
            with pytest.raises(CoinpaprikaAPIException):
                data_loader.load_data_from_api(datetime(2008, 2, 1), datetime(2012, 2, 3), 'btc-bitcoin')

    def test_update_dictionary_with_name(self, data_loader):
        empty_dict = {}
        data_loader.update_dictionary_with_name(empty_dict, 'btc-bitcoin')
        assert empty_dict['name'] == 'btc-bitcoin'

    def test_modify_data(self, data_loader):
        data_loader.data = api_content
        data_loader.modify_data('btc-bitcoin')
        assert data_loader.data[0]['name'] == 'btc-bitcoin'
