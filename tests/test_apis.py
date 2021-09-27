import datetime
import pytest
import requests

from src.apis import ApiMercadoBitcoin, ApiDaySummary
from unittest.mock import patch


@pytest.fixture
@patch("src.apis.ApiMercadoBitcoin.__abstractmethods__", set())
def fixture_api():
    return ApiMercadoBitcoin(coin="ND")


def mocked_requests_get(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, status_code, json_data):
            super().__init__()
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception

    if args[0] == "Response success.":
        return MockResponse(status_code=200, json_data={"foo": "bar"})
    else:
        return MockResponse(status_code=404, json_data=None)


class TestApiMercadoBitcoin:
    @patch("requests.get")
    @patch("src.apis.ApiMercadoBitcoin._get_endpoint", return_value="Request done.")
    def test_get_data_request(self, mock_get_endpoint, mock_requests, fixture_api):
        fixture_api.get_data()

        mock_requests.assert_called_once_with("Request done.")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("src.apis.ApiMercadoBitcoin._get_endpoint", return_value="Response success.")
    def test_get_data_response_success(
        self, mock_get_endpoint, mock_requests, fixture_api
    ):
        actual = fixture_api.get_data()
        expected = {"foo": "bar"}

        assert actual == expected

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch("src.apis.ApiMercadoBitcoin._get_endpoint", return_value="Response failure.")
    def test_get_data_response_failure(
        self, mock_get_endpoint, mock_requests, fixture_api
    ):
        with pytest.raises(Exception):
            fixture_api.get_data()


class TestApiDaySummary:
    @pytest.mark.parametrize(
        "coin, date, expected",
        [
            (
                "BTC",
                datetime.date(2021, 6, 15),
                "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/15",
            ),
            (
                "ETH",
                datetime.date(2021, 6, 15),
                "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/15",
            ),
            (
                "ETH",
                datetime.date(2021, 6, 30),
                "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/30",
            ),
        ],
    )
    def test_get_endpoint(self, coin, date, expected):
        api = ApiDaySummary(coin=coin)
        actual = api._get_endpoint(date=date)

        assert actual == expected
