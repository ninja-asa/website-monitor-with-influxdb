import os

# Define configuration of influxdb connections. If env var are not set use default values
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
TOKEN = os.getenv("INFLUX_TOKEN", "<your-influxdb-token>")
ORG = os.getenv("INFLUX_ORG", "<your-influxdb-org>")
BUCKET = os.getenv("INFLUX_BUCKET", "<your-influxdb-bucket>")
# BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1000))
# FLUSH_INTERVAL = int(os.getenv("FLUSH_INTERVAL", 5 * 60 * 1000))  # 5 minutes in milliseconds
