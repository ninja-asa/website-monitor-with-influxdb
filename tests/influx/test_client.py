import pytest
from influxdb_client import InfluxDBClient, Point, WriteApi
from datetime import datetime
from unittest.mock import Mock, patch

from webmonitor.influx.client import write_website_availability_to_influxdb
from webmonitor.monitor.monitor import WebsiteStatus
from webmonitor.influx.config import INFLUX_URL, TOKEN, ORG, BUCKET

@pytest.fixture
def mock_influxdb_client(monkeypatch) -> tuple[Mock, Mock]:
    # Mock the InfluxDBClient and write_api objects
    mock_client = Mock(spec=InfluxDBClient)
    mock_write_api = Mock(spec=WriteApi)
    monkeypatch.setattr("webmonitor.influx.client.InfluxDBClient", mock_client)
    monkeypatch.setattr("webmonitor.influx.client.write_api", mock_write_api)
    mock_write_api.write = Mock()    # Ensure write is a mock object
    return mock_client, mock_write_api
    
@patch('webmonitor.influx.client.datetime')
def test_write_website_availability_to_influxdb(mock_datetime, mock_influxdb_client):
    # Arrange
    mock_datetime.now.return_value = datetime(2021, 9, 1, 12, 0, 0)
    website = "example.com"
    status = WebsiteStatus(success=True, response_code=200, response_time=0.5, connection_time=0.2)
    _, mock_write_api = mock_influxdb_client

    # Act
    write_website_availability_to_influxdb(website, status)

    # Assert
    current_time = mock_datetime.now.return_value
    expected_point = Point("website_status") \
        .tag("website", website) \
        .field("success", int(status.success)) \
        .field("response_code", status.response_code) \
        .field("response_time", status.response_time) \
        .field("connection_time", status.connection_time) \
        .time(current_time, write_precision="s") 

    call_args = mock_write_api.write.call_args
    called_bucket = call_args[1]['bucket']
    called_org = call_args[1]['org']
    called_record = call_args[1]['record']
    called_write_precision = call_args[1]['write_precision']

    assert called_bucket == BUCKET, f"called_bucket: {called_bucket}, BUCKET: {BUCKET}"
    assert called_org == ORG, f"called_org: {called_org}, ORG: {ORG}"
    assert called_write_precision == 's', f"called_write_precision: {called_write_precision}, expected: 's'"
    assert called_record.to_line_protocol() == expected_point.to_line_protocol(), f"called_record: {called_record.to_line_protocol()}, expected_point: {expected_point.to_line_protocol()}"