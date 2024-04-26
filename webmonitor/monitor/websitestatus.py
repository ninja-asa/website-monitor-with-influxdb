from dataclasses import dataclass

@dataclass
class WebsiteStatus:
    """
    Represents the status of a website after monitoring.

    Attributes:
        success (bool): Indicates whether the website check was successful.
        response_code (int): The HTTP status code returned by the website (e.g., 200, 404).
        response_time (float): The total time taken for the server to process the request and send back a response, 
            including connection time, in seconds.
        connection_time (float): The time taken to establish a connection with the server, in seconds.
    """
    success: bool
    response_code: int
    response_time: float
    connection_time: float