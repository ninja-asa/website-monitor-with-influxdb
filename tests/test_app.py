from unittest.mock import patch
from webmonitor.app import monitor_websites, WebsiteStatus

@patch('webmonitor.app.write_website_availability_to_influxdb')
@patch('webmonitor.app.MonitorWebsite')
def test_monitor_websites(mock_monitor_website, mock_write_website_availability_to_influxdb):
    # Arrange
    mock_monitor = mock_monitor_website.return_value
    mock_monitor.url = "http://example.com"
    mock_monitor.check.return_value = WebsiteStatus(success=True, response_code=200, response_time=0.5, connection_time=0.2)

    # Act
    monitor_websites([mock_monitor])

    # Assert
    mock_monitor.check.assert_called_once()
    mock_monitor.check.assert_called_with()
    mock_write_website_availability_to_influxdb.assert_called_once()
    mock_write_website_availability_to_influxdb.assert_called_with(
        mock_monitor.url, mock_monitor.check.return_value)
