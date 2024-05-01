from threading import Timer
import logging 

from webmonitor.monitor.exceptions import NoInternetConnectionError
from webmonitor.monitor.monitor import MonitorWebsite, WebsiteStatus
from webmonitor.influx.client import write_website_availability_to_influxdb
from webmonitor.influx.exceptions import UnknownInfluxDBClientError

from webmonitor.config import WEBSITES, CHECK_INTERVAL
from webmonitor.mylogger import configure_logging, logging

configure_logging(filename=f"{__name__}.log", level=logging.INFO)

def monitor_websites(monitors: list[MonitorWebsite]) -> None:
    """Monitor websites in parallel

    Args:
        monitors (list[MonitorWebsite]): List of MonitorWebsite objects
    """
    for monitor in monitors:
        logging.info(f"Checking {monitor.url}")
        try:
            website_status: WebsiteStatus = monitor.check()
            logging.info(f"{monitor.url} is {'up' if website_status.success else 'down'}")
            write_website_availability_to_influxdb(monitor.url, website_status)
        except NoInternetConnectionError:
            logging.error(f"No internet connection")
        except UnknownInfluxDBClientError as error:
            logging.error(f"Unknown InfluxDB client error: {error}")
        except Exception as error:
            logging.error(f"Unknown error: {error}")
        logging.info("-" * 50)
    return

def run_monitor() -> None:
    """Run the website monitor"""
    monitors = [MonitorWebsite(url) for url in WEBSITES]
    # Print configuration of the monitor
    logging.info("-" * 50)
    logging.info(f"Monitoring websites: {WEBSITES}")
    logging.info(f"Checking every {CHECK_INTERVAL} seconds")
    logging.info("-" * 50)

    monitor_websites(monitors)
    timer = Timer(CHECK_INTERVAL, run_monitor)
    timer.start()

run_monitor()