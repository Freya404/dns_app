from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)


def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    """Return the Fibonacci number for the given sequence number."""
    number = request.args.get('number')
    if number is None or not number.isdigit():
        return jsonify(error="Invalid or missing 'number' parameter"), 400

    fib_number = fibonacci(int(number))
    return jsonify(fibonacci=fib_number), 200


def register_with_as(hostname, fs_ip, as_ip, as_port):
    """
    Register the FS hostname with the AS via UDP and wait for a confirmation response.

    Args:
    - hostname: The hostname to register (e.g., "fibonacci.com").
    - fs_ip: The IP address of this Fibonacci Server.
    - as_ip: The IP address of the Authoritative Server.
    - as_port: The port number of the Authoritative Server.
    """
    # Construct the registration message
    message = f"TYPE=A\nNAME={hostname}\nVALUE={fs_ip}\nTTL=10"

    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Send the registration message to the AS
        udp_socket.sendto(message.encode(), (as_ip, int(as_port)))
        print(f"Sent registration message to AS at {as_ip}:{as_port}")

        # Optionally set a timeout for the response (e.g., 10 seconds)
        udp_socket.settimeout(10)

        try:
            # Wait for a response from the AS
            response, _ = udp_socket.recvfrom(1024)
            print(f"Received confirmation from AS: {response.decode()}")
        except socket.timeout:
            print("No confirmation received from AS within the timeout period.")


def start_fs(hostname, fs_ip, as_ip, as_port):
    """
    Start the Fibonacci Server and register with the Authoritative Server.

    Args are the same as in `register_with_as`.
    """
    # Register with the AS in a separate thread to not block the server start
    threading.Thread(target=register_with_as, args=(hostname, fs_ip, as_ip, as_port)).start()
    app.run(host='0.0.0.0', port=9090)


if __name__ == '__main__':
    # Example configuration - replace with actual values
    HOSTNAME = "fibonacci.com"
    FS_IP = "127.0.0.1"  # The FS's own IP address
    AS_IP = "127.0.0.1"  # The AS's IP address
    AS_PORT = 53533  # The AS's listening port

    start_fs(HOSTNAME, FS_IP, AS_IP, AS_PORT)
