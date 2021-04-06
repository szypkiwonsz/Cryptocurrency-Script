from datetime import datetime

import pytest

from utils import date_with_last_day_of_month


@pytest.mark.utils
class TestUtils:

    def test_date_with_last_day_of_month(self):
        assert date_with_last_day_of_month(datetime(2012, 1, 1)) == datetime(2012, 1, 31)
        assert date_with_last_day_of_month(datetime(2012, 2, 1)) == datetime(2012, 2, 29)
