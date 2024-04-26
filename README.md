# Website Availability Monitor
[![Website Monitor - Publish Docker Image](https://github.com/ninja-asa/website-monitor-with-influxdb/actions/workflows/publish-website-monitor-docker-image.yml/badge.svg?event=registry_package)](https://github.com/ninja-asa/website-monitor-with-influxdb/actions/workflows/publish-website-monitor-docker-image.yml)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/gpl-2.0)


This Python script monitors the availability of one or more websites by periodically checking their health endpoints. It writes the availability status to an InfluxDB database for further analysis and visualization.

## Features

- Checks the availability of one or more websites at regular intervals.
- Configurable number of retries before considering a check as failed.
- Verifies internet connectivity before initiating website health checks.
- Writes website availability status to an InfluxDB database.

## Prerequisites

- Visual Studio Code with the Remote - Containers extension installed.
- Docker installed on your system.

## Getting Started
### Start a Docker Container
1. Clone this repository.
2. Open the project in Visual Studio Code.
3. Build Docker Image using the provided `Dockerfile`:
    ```bash
    docker build -t website-availability-monitor .
    ```
4. Copy the `example.env` file to a `.env` the relevant environment variables - your InfluxDB connection parameters and the websites you want to monitor.
5. Run the Docker container:
    ```bash
    docker run --env-file .env website-availability-monitor
    ```

### Develop within IDE using Devcontainer
1. Clone this repository
2. Open the project in Visual Studio Code.

3. When prompted, reopen the project in a container using the provided `.devcontainer` configuration.

4. Install required Python packages by running the following command in the terminal:

    ```bash
    pip install -r requirements.txt
    ```

5. Copy the `example.env` file to a `.env` the relevant environment variables - your InfluxDB connection parameters and the websites you want to monitor.
6. Launch the debugger by selecting the adequate configuration. It will load the environment variables from the `.env` file and start the script.

## Configuration

All the required configuration is done through the definition of environment variables, which can be consulted in `example.env`.


## Data Schema for InfluxDB

The data written into InfluxDB is structured as follows:

### Measurement
The measurement name is website_status.

### Tags
- website: The name of the website being monitored.
### Fields
- success: A boolean value (represented as an integer, 0 for False and 1 for True) indicating whether the website is up (1) or down (0).
- response_code: The HTTP response code received when trying to access the website.
- response_time: The time taken to receive the HTTP response from the website.
- connection_time: The time taken to establish a connection to the website.
## Time
- The timestamp (time) for each data point is the current time when the data is written to InfluxDB. The precision is set to seconds.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [GNU General Public License Version 2](..\LICENSE).
