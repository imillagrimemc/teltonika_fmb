# Readme for TCP Server for Tracker Data

This README provides an overview of the code for a TCP server designed to receive and process tracker data from connected devices. The code is written in Python and uses the `socket` library for network communication, `psycopg2` for PostgreSQL database interaction, and `twos_complement` for handling two's complement conversions.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Code Explanation](#code-explanation)
- [Usage](#usage)

## Prerequisites

Before using this code, ensure you have the following prerequisites:

- Python 3.x installed on your system.
- PostgreSQL database with the necessary schema and permissions.
- The `psycopg2` library installed (`pip install psycopg2-binary`).

## Configuration

Before running the code, you need to configure it according to your specific setup. Open the Python script and modify the following variables in the script:

- `SERVER`: Replace `"YOUR_IP"` with the IP address or hostname where you want the server to bind.
- `PORT`: Replace `YOUR_PORT` with the port number on which the server should listen.
- Database Configuration:
  - `db_url`: Replace `"localhost"` with the database server's hostname or IP address.
  - `db_port`: Replace `5432` with the PostgreSQL server port.
  - `db_name`: Replace `"gumbaz_db"` with the name of your PostgreSQL database.
  - `db_username`: Replace `"gumbaz_user"` with the database username.
  - `db_password`: Replace `"gumbaz_password"` with the database password.

## Code Explanation

Here's an overview of the key components and functions in the code:

1. `decodethis(data, imei)`: This function decodes tracker data received as a hexadecimal string. It extracts various data fields, such as length, record, timestamp, priority, longitude, latitude, altitude, angle, satellites, and speed. The decoded data is then inserted into a PostgreSQL database.

2. `loc_convert(loc)`: This function converts a location value from a binary format (two's complement) to a floating-point longitude or latitude value.

3. `handle_client(conn, addr)`: This function handles each incoming client connection. It receives the IMEI (International Mobile Equipment Identity) from the client, acknowledges the connection, and continuously receives data from the client. The received data is decoded using `decodethis()`.

4. `start()`: This function starts the server, binds it to the specified IP address and port, and listens for incoming client connections. Each connection is handled in a separate thread.

5. Main section: The script creates a socket, binds it to the configured IP address and port, and starts the server using the `start()` function.

## Usage

1. Configure the script as described in the "Configuration" section.

2. Run the script using Python: `python your_script_name.py`.

3. The server will start listening on the specified IP address and port.

4. Connect your tracker devices to the server using the specified IP address and port.

5. The server will receive tracker data, decode it, and insert it into the PostgreSQL database.

6. You can monitor incoming connections and data processing in the console.

Make sure that your PostgreSQL database is set up with the correct schema and table structure to store the tracker data.
