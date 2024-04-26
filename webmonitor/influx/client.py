from influxdb_client import InfluxDBClient, Point, WriteApi
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

from webmonitor.influx.config import INFLUX_URL, TOKEN, ORG, BUCKET
from webmonitor.influx.exceptions import UnknownInfluxDBClientError
from webmonitor.monitor.monitor import WebsiteStatus

client = InfluxDBClient(url=INFLUX_URL, token=TOKEN)

write_api: WriteApi = client.write_api(write_options=SYNCHRONOUS)

def write_website_availability_to_influxdb(website: str, status: WebsiteStatus) -> None:
    """Write website availability to influxdb

    Args:
        website (str): name of the website
        status (bool): whether the website is up or down
    """
    current_time = datetime.now()
    
    try: 
        point = Point("website_status") \
            .tag("website", website) \
            .field("success", int(status.success)) \
            .field("response_code", status.response_code) \
            .field("response_time", status.response_time) \
            .field("connection_time", status.connection_time) \
            .time(current_time, write_precision="s")
        write_api.write(bucket=BUCKET, org=ORG, record=point, write_precision='s')    
    except Exception as error:
        raise UnknownInfluxDBClientError(f"Unknown error: {error}")
    return
