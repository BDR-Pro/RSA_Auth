# Project: Login with PEM Private Key (Local Proxy Server Example)

## Overview

This Flask-based project demonstrates a secure login mechanism using a PEM private key for authentication. It serves as a client application that interacts with a local proxy server (assumed to be running on port 8000) to retrieve data. The authentication process involves generating and verifying challenges along with a digital signature.

## Features

- **Secure Authentication**: Users authenticate themselves using a digital signature generated from a PEM private key.
- **Session Management**: Sessions are managed securely using Flask's session management with a customizable lifetime.
- **Challenge-Based Authentication**: Users are challenged with a randomly generated string during authentication to prevent replay attacks.
- **Proxy Server Interaction**: The application interacts with a local proxy server running on port 8000 to fetch data.

## Usage

1. **Setup PEM Private Key**:
   - Ensure you have a PEM private key for authentication. This key should be securely stored and managed.

2. **Install Dependencies**:
   1- Install the required dependencies specified in `requirements.txt` using pip:

     ```bash
     pip install -r requirements.txt
     ```

3. **Configure Public Key**:
   - Set up the public key of the proxy server. Update `public_key.pem` with the appropriate public key.

4. **Run the Application**:
   1- Execute the Python script `app.py`:

     ```bash
     python app.py
     ```

5. **Access the Application**:
   - Open a web browser and navigate to `http://localhost:<port>` to access the application.

6. **Authentication**:
   - Click on the login button to initiate the authentication process.
   - Upon successful authentication, you'll gain access to the status page displaying data fetched from the proxy server.

## Files

- **app.py**: Main Python script containing the Flask application.
- **public_key.pem**: Public key of the proxy server for signature verification.
- **templates/**: Directory containing HTML templates for rendering pages.
- **challenge.txt**: File storing challenges for authentication.

## Notes

- Ensure the local proxy server is running on port 8000 for successful data retrieval.
- Customize session lifetime and other configurations in `app.py` as needed.
- This project serves as a demonstration and should be extended and modified for production use, including enhanced security measures and error handling.

## Example

### Author

- [Bader Alotaibi](github.com/bdr-pro)

### License

- This project is licensed under the MIT. See the LICENSE file for details.

### Acknowledgments

- Mention any acknowledgments or credits for libraries, resources, or inspiration used in the project
