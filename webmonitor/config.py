import os

WEBSITES = os.getenv("WEBSITES", "https://www.google.com/,https://www.google.com/").split(",")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 10)) # seconds
