from datetime import datetime
from unittest.mock import patch, mock_open

import pytest
from click.testing import CliRunner
from dateutil.relativedelta import relativedelta
from httmock import HTTMock, all_requests

from script import average_price_by_month, consecutive_increase, export
from tests.conftest import api_content


@all_requests
def api_mock(url, request):
    return {'status_code': 200,
            'content': api_content}


runner = CliRunner()


@pytest.mark.script
class TestAveragePriceByMonth:

    def test_average_price_by_month(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                response = runner.invoke(average_price_by_month, ['--start_date=2012-01', '--end_date=2012-02'])
                assert response.exit_code == 0
                assert '5.48' in response.output

    def test_average_price_by_month_diff_coin(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                response = runner.invoke(average_price_by_month, [
                    '--start_date=2012-01', '--end_date=2012-02', '--coin=usdt-tether'])
                assert response.exit_code == 0
                assert '5.48' in response.output

    def test_average_price_by_month_too_early_start_date(self):
        response = runner.invoke(average_price_by_month, [f'--start_date=2008-12-31', f'--end_date=2011-12'])
        assert response.exit_code == 2

    def test_average_price_by_month_too_late_start_date(self):
        next_month = datetime.now() + relativedelta(months=1)
        response = runner.invoke(average_price_by_month, [f'--start_date={str(next_month)[:7]}', f'--end_date=2011-12'])
        assert response.exit_code == 2

    def test_average_price_by_month_too_late_end_date(self):
        next_month = datetime.now() + relativedelta(months=1)
        response = runner.invoke(average_price_by_month, ['--start_date=2012-01', f'--end_date={str(next_month)[:7]}'])
        assert response.exit_code == 2

    def test_average_price_by_month_end_date_before_start_date(self):
        response = runner.invoke(average_price_by_month, ['--start_date=2012-01', f'--end_date=2011-12'])
        assert response.exit_code == 2

    def test_average_price_by_month_wrong_arguments(self):
        response = runner.invoke(average_price_by_month, ['--start_date=2012-01-01', f'--end_date=2011-12-01'])
        assert response.exit_code == 2


@pytest.mark.script
class TestConsecutiveIncrease:

    def test_consecutive_increase(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                response = runner.invoke(consecutive_increase, ['--start_date=2012-01-01', '--end_date=2012-02-03'])
                assert response.exit_code == 0
                assert '$17.66' in response.output

    def test_consecutive_increase_diff_coin(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                response = runner.invoke(consecutive_increase, [
                    '--start_date=2012-01-01', '--end_date=2012-02-03', '--coin=usdt-tether'
                ])
                assert response.exit_code == 0
                assert '$17.66' in response.output

    def test_average_price_by_month_too_early_start_date(self):
        response = runner.invoke(consecutive_increase, [
            f'--start_date=2008-12-31', f'--end_date=2011-12-01'
        ])
        assert response.exit_code == 2

    def test_average_price_by_month_too_late_start_date(self):
        next_month = datetime.now() + relativedelta(months=1)
        response = runner.invoke(consecutive_increase, [
            f'--start_date={str(next_month)[:10]}', f'--end_date=2011-12-01'
        ])
        assert response.exit_code == 2

    def test_consecutive_increase_too_late_end_date(self):
        next_month = datetime.now() + relativedelta(months=1)
        response = runner.invoke(consecutive_increase, [
            '--start_date=2012-01-01', f'--end_date={str(next_month)[:10]}'
        ])
        assert response.exit_code == 2

    def test_consecutive_increase_end_date_before_start_date(self):
        response = runner.invoke(consecutive_increase, ['--start_date=2012-01-01', f'--end_date=2011-12-01'])
        assert response.exit_code == 2

    def test_consecutive_increase_wrong_arguments(self):
        response = runner.invoke(consecutive_increase, ['--start_date=2012-01', f'--end_date=2011-12'])
        assert response.exit_code == 2


@pytest.mark.script
class TestExport:

    def test_export_json(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                with patch('data_exporters.open', mock_open()) as mocked_file:
                    response = runner.invoke(export, [
                        '--start_date=2012-01-01', '--end_date=2012-02-03', '--format_type=json', '--file=data.json'
                    ])
                    mocked_file.assert_called_once_with('data.json', 'w')
                assert response.exit_code == 0
                assert 'data.json' in response.output

    def test_export_json_diff_coin(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                with patch('data_exporters.open', mock_open()) as mocked_file:
                    response = runner.invoke(export, [
                        '--start_date=2012-01-02', '--end_date=2012-02-04', '--format_type=json', '--file=data.json',
                        '--coin=usdt-tether'
                    ])
                    mocked_file.assert_called_once_with('data.json', 'w')
                assert response.exit_code == 0
                assert 'data.json' in response.output

    def test_export_csv(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                with patch('data_exporters.open', mock_open()) as mocked_file:
                    response = runner.invoke(export, [
                        '--start_date=2012-01-01', '--end_date=2012-02-03', '--format_type=csv', '--file=data.csv'
                    ])
                    mocked_file.assert_called_once_with('data.csv', 'w', newline='')
                assert response.exit_code == 0
                assert 'data.csv' in response.output

    def test_export_csv_diff_coin(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                with patch('data_exporters.open', mock_open()) as mocked_file:
                    response = runner.invoke(export, [
                        '--start_date=2012-01-02', '--end_date=2012-02-04', '--format_type=csv', '--file=data.csv',
                        '--coin=usdt-tether'
                    ])
                    mocked_file.assert_called_once_with('data.csv', 'w', newline='')
                assert response.exit_code == 0
                assert 'data.csv' in response.output

    def test_export_json_without_extension(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                with patch('data_exporters.open', mock_open()) as mocked_file:
                    response = runner.invoke(export, [
                        '--start_date=2012-01-01', '--end_date=2012-02-03', '--format_type=json', '--file=data'
                    ])
                    mocked_file.assert_called_once_with('data.json', 'w')
                assert response.exit_code == 0
                assert 'data.json' in response.output

    def test_export_csv_without_extension(self, database):
        with patch('database_handler.DatabaseHandler.db') as mock:
            mock.return_value = database
            with HTTMock(api_mock):
                with patch('data_exporters.open', mock_open()) as mocked_file:
                    response = runner.invoke(export, [
                        '--start_date=2012-01-02', '--end_date=2012-02-04', '--format_type=csv', '--file=data',
                        '--coin=usdt-tether'
                    ])
                    mocked_file.assert_called_once_with('data.csv', 'w', newline='')
                assert response.exit_code == 0
                assert 'data.csv' in response.output

    def test_average_price_by_month_too_early_start_date(self):
        response = runner.invoke(export, [
            f'--start_date=2008-12-31', f'--end_date=2011-12-01', '--format_type=json', '--file=data.json'
        ])
        assert response.exit_code == 2

    def test_average_price_by_month_too_late_start_date(self):
        next_month = datetime.now() + relativedelta(months=1)
        response = runner.invoke(export, [
            f'--start_date={str(next_month)[:10]}', f'--end_date=2011-12-01', '--format_type=json', '--file=data.json'
        ])
        assert response.exit_code == 2

    def test_export_too_late_end_date(self):
        next_month = datetime.now() + relativedelta(months=1)
        response = runner.invoke(export, [
            '--start_date=2012-01-01', f'--end_date={str(next_month)[:10]}', '--format_type=json', '--file=data.json'
        ])
        assert response.exit_code == 2

    def test_export_end_date_before_start_date(self):
        response = runner.invoke(export, ['--start_date=2012-01-01', f'--end_date=2011-12-01'])
        assert response.exit_code == 2

    def test_export_wrong_arguments(self):
        response = runner.invoke(export, [
            '--start_date=2012-01-01', f'--end_date=2011-12-01', '--format_type=wrong', '--file=data.json'
        ])
        assert response.exit_code == 2
