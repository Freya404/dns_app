from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

def query_dns_server(hostname, as_ip, as_port):
    """Query the DNS server for the IP address of a given hostname."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        query = f"TYPE=A\nNAME={hostname}"
        udp_socket.sendto(query.encode(), (as_ip, int(as_port)))
        response, _ = udp_socket.recvfrom(1024)
        return response.decode()

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Validate parameters
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify(error="Missing parameters"), 400

    try:
        # Convert number to int and validate
        number = int(number)
    except ValueError:
        return jsonify(error="Invalid number parameter"), 400

    # Query DNS server for FS IP address
    dns_response = query_dns_server(hostname, as_ip, as_port)
    lines = dns_response.split('\n')
    fs_ip = next((line.split('=')[1] for line in lines if line.startswith('VALUE')), None)

    if not fs_ip:
        return jsonify(error="DNS query failed or FS not found"), 404

    # Request Fibonacci number from FS
    try:
        fs_response = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")
        fs_response.raise_for_status()  # Raises error for HTTP errors
        return fs_response.content, 200
    except requests.RequestException as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
