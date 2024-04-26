import requests
from typing import Literal
import time

from webmonitor.monitor.websitestatus import WebsiteStatus
from webmonitor.monitor.config import RETRIES, CONTROL_WEBSITE
from webmonitor.monitor.exceptions import NoInternetConnectionError, UnknownMonitorError

class MonitorWebsite():
    timeout = 15 # seconds

    def __init__(self, url: str) -> None:
        """Monitor a website

        Args:
            url (str): URL of the website to monitor
        """
        self.url = url
        self.retries = RETRIES
        self.control_website = CONTROL_WEBSITE

    def check(self) -> WebsiteStatus:
        """Check if the website is up

        Raises:
            error: NoInternetConnectionError

        Returns:
            bool: True if the website is up, False otherwise
        """
        try:
            self.check_internet_connection()
            return self.check_connection(self.url)
        except NoInternetConnectionError as error:
            raise error
        # in case of other errors, raise UnknownMonitorError
        except Exception as error:
            raise UnknownMonitorError(f"Unknown error: {error}")
                
    def check_connection(self, url) -> WebsiteStatus:
        """Check if can connect to provided website. Retries if necessary.

        Args:
            url (str): URL of the website to check

        Returns:
            bool: True if can connect, False otherwise. If between 200 and 300, return True.
        """
        success = False
        for _ in range(self.retries):
            try:
                start_time = time.time()
                response = requests.get(url=url, timeout=self.timeout)
                end_time = time.time()
                response_time = end_time - start_time
                connection_time = response.elapsed.total_seconds()
                status_code = response.status_code
                if 200 <= status_code < 300:  # 200 OK
                    success = True
                    response_code = status_code
                    break
            except requests.RequestException as error:
                continue
        return WebsiteStatus(success, response_code, response_time, connection_time)
    

    def check_internet_connection(self) -> Literal[True]:
        """Check if can connect to the control website

        Raises:
            NoInternetConnectionError: If cannot connect to the control website, raise this error

        Returns:
            bool: True if can connect, False otherwise
        """
        if not self.check_connection(self.control_website).success:
            raise NoInternetConnectionError(f"No internet connection - cannot connect to {self.control_website}")
        return True
        
    def get_url(self) -> str:
        return self.url

    def __str__(self)-> str:
        return f"URL: {self.url}, Retries: {self.retries}, Control Website: {self.control_website}"


if __name__ == "__main__":
    monitors = [MonitorWebsite(CONTROL_WEBSITE)] 
    while True:
        for monitor in monitors:
            print(monitor)
            print(f"Connection to {monitor.get_url()} is {'UP' if monitor.check() else 'DOWN'}")
            print("\n")