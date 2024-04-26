# Specifying the base image
FROM python:3.11-buster

# Install system dependencies and pip
RUN apt-get update -y && apt-get install --no-install-recommends -y \
    python3-pip

RUN apt install nano -y

# Installing the requirements.txt
RUN pip install --upgrade pip

# Install local package and its requirements
COPY . /workspace
WORKDIR /workspace
RUN pip install .

# Set labels
LABEL org.opencontainers.image.source=https://github.com/ninja-asa/influxdb-getting-started/
LABEL org.label-schema.vcs-url=https://github.com/ninja-asa/influxdb-getting-started/

LABEL org.opencontainers.image.description="Container which launches a recurrent web monitoring service and writes the results to an InfluxDB database."
LABEL org.label-schema.description="Container which launches a recurrent web monitoring service and writes the results to an InfluxDB database."

LABEL org.opencontainers.image.licenses="GNU General Public License Version 2"

LABEL org.label-schema.schema-version="1.0"

LABEL org.label-schema.docker.cmd="docker run -d -e INFLUX_URL=<Url> -e INFLUX_TOKEN=<YourToken> -e INFLUX_BUCKET=<YourBucket> -e INFLUX_ORG=<Your Org> -e CHECK_INTERVAL=60 -e WEBSITES=<Your websites> -e CONTROL_WEBSITE=https://www.google.com -e RETRIES=3 ninjaasa/influxdb-getting-started-website-monitor"

LABEL org.opencontainers.image.authors="Sofia Assis"

LABEL org.opencontainers.image.title="InfluxDB Getting Started - Website Monitor"
LABEL org.label-schema.title="InfluxDB Getting Started - Website Monitor"

# Start the application
CMD ["python", "webmonitor/app.py"]
