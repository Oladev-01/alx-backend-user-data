
# 0x01. Basic Authentication

## Overview

This project demonstrates the implementation of basic authentication mechanisms for securing web applications. It covers several types of authentication, including HTTP Digest Authentication and Bearer Token Authentication. The goal is to understand how to secure endpoints and manage authentication headers effectively.

## Features

- **Basic Authentication**: Authenticate users by sending username and password in the `Authorization` header.
- **Digest Authentication**: Use HTTP Digest Authentication to securely transmit credentials.
- **Bearer Token Authentication**: Implement token-based authentication for API access.

## Getting Started

### Prerequisites

- **Python 3.x**: Ensure Python 3 is installed on your machine.
- **Flask**: A micro web framework for Python used to create the application.
- **Flask-HTTPAuth**: An extension for Flask that provides basic and digest authentication.

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/0x01-basic-authentication.git
    cd 0x01-basic-authentication
    ```

2. **Install Dependencies**:

    It's recommended to use a virtual environment. Install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

    Ensure that `requirements.txt` includes:

    ```text
    Flask
    Flask-HTTPAuth
    ```

### Configuration

1. **Set Up Environment Variables**:

    Configure the following environment variables for authentication:

    ```bash
    export PERSONAL_DATA_DB_USERNAME=root
    export PERSONAL_DATA_DB_PASSWORD=root
    export PERSONAL_DATA_DB_HOST=localhost
    export PERSONAL_DATA_DB_NAME=my_db
    ```

    Adjust these values according to your database setup.

2. **Run the Application**:

    Start the Flask application:

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

### Usage

- **Basic Authentication**: Access the endpoint by including the `Authorization` header with base64-encoded credentials.

    ```bash
    curl -u username:password http://127.0.0.1:5000/
    ```

- **Digest Authentication**: Use the `curl` command with the `--digest` option.

    ```bash
    curl -u username:password --digest http://127.0.0.1:5000/
    ```

- **Bearer Token Authentication**: Include the `Authorization` header with a bearer token.

    ```bash
    curl -H "Authorization: Bearer your-token" http://127.0.0.1:5000/
    ```

### Testing

Run the provided test scripts to validate authentication mechanisms. Ensure that your Flask application is running before executing tests.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes. Ensure that your changes are well-documented and tested.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


