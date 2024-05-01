import pytest
import requests_mock
import requests
from unittest.mock import patch
from webmonitor.monitor.monitor import MonitorWebsite, WebsiteStatus
from webmonitor.monitor.exceptions import NoInternetConnectionError, UnknownMonitorError

@pytest.mark.parametrize("status_code, expected", [
    (200, True),
    (201, True),
    (300, False),
    (400, False),
    (500, False),
])
def test_check_connection_get_with_response(status_code, expected):
    with requests_mock.Mocker() as m:
        m.get('http://example.com', status_code=status_code)
        monitor = MonitorWebsite('http://example.com')
        status = monitor.check_connection('http://example.com')
        assert status.success == expected
        assert status.response_code == status_code

@pytest.mark.parametrize("exception", [
    requests.RequestException,
    requests.Timeout,
    requests.ConnectionError,
])
def test_check_connection_get_with_exception(exception):
    with requests_mock.Mocker() as m:
        m.get('http://example.com', exc=exception)
        monitor = MonitorWebsite('http://example.com')
        status = monitor.check_connection('http://example.com')
        assert not status.success
        assert status.response_code == 0

@patch('webmonitor.monitor.monitor.CONTROL_WEBSITE', new='http://example.com')
def test_check_internet_connection() -> None:
    with requests_mock.Mocker() as m:
        m.get('http://example.com', status_code=200)
        monitor = MonitorWebsite('http://example.com')
        assert monitor.check_internet_connection()

@patch('webmonitor.monitor.monitor.CONTROL_WEBSITE', new='http://example.com')
def test_check_internet_connection_no_connection():
    with requests_mock.Mocker() as m:
        m.get('http://example.com', status_code=400)
        monitor = MonitorWebsite('http://example.com')
        with pytest.raises(NoInternetConnectionError):
            monitor.check_internet_connection()
    
def test_get_url():
    monitor = MonitorWebsite('http://example.com')
    assert monitor.get_url() == 'http://example.com'

@patch.object(MonitorWebsite, 'check_internet_connection', return_value=True)
@patch.object(MonitorWebsite, 'check_connection', return_value=WebsiteStatus(True, 200, 0.5, 0.2))
def test_check(mock_check_connection, mock_check_internet_connection):
    with requests_mock.Mocker() as m:
        m.get('http://example.com', status_code=200)
        monitor = MonitorWebsite('http://example.com')
        status = monitor.check()
        mock_check_internet_connection.assert_called_once()
        mock_check_connection.assert_called_once_with('http://example.com')
        assert status.success
        assert status.response_code == 200
    
