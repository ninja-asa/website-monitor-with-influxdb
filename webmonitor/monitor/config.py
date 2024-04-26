import os

# Define configuration of monitor connections. If env var are not set use default values
CONTROL_WEBSITE = os.getenv("CONTROL_WEBSITE", "https://www.google.com")
# number of retries before registering a fail
RETRIES = int(os.getenv("RETRIES", 3))
