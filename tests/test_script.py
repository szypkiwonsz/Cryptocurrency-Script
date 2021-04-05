from datetime import datetime
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from dateutil.relativedelta import relativedelta
from httmock import HTTMock, all_requests

from script import average_price_by_month
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
