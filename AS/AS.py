import socket
import json
import os

DNS_RECORDS_FILE = 'dns_records.json'


def start_authoritative_server():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Bind the socket to all interfaces on port 53533
        udp_socket.bind(('0.0.0.0', 53533))
        print("Authoritative Server listening on port 53533")

        while True:
            # Wait for an incoming registration message
            message, client_address = udp_socket.recvfrom(1024)
            print(f"Received message from {client_address}: {message.decode()}")

            # Process the registration message (not shown here for brevity)
            handle_incoming_message(message.decode(), client_address)

            # Send a confirmation response back to the sender
            confirmation_message = "Registration successful"
            udp_socket.sendto(confirmation_message.encode(), client_address)


def load_dns_records():
    """Load DNS records from a JSON file."""
    try:
        with open(DNS_RECORDS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_dns_records(records):
    filepath = os.path.join(os.getcwd(), DNS_RECORDS_FILE)
    print(f"Saving DNS records to: {filepath}")  # Print the file path
    with open(filepath, 'w') as file:
        json.dump(records, file, indent=4)


def process_registration(data):
    """Process a registration request."""
    records = load_dns_records()
    records[data['NAME']] = {'IP': data['VALUE'], 'TTL': data['TTL']}
    save_dns_records(records)
    return "Registration successful"


def process_query(data):
    """Process a DNS query."""
    records = load_dns_records()
    record = records.get(data['NAME'], {})
    if record:
        response = f"TYPE=A\nNAME={data['NAME']}\nVALUE={record['IP']}\nTTL={record['TTL']}"
    else:
        response = "Record not found"
    return response


def handle_message(message):
    """Handle incoming messages and route them to the appropriate function."""
    lines = message.strip().split('\n')
    data = {line.split('=')[0]: line.split('=')[1] for line in lines}

    if 'VALUE' in data:  # Registration request
        return process_registration(data)
    else:  # DNS query
        return process_query(data)

def handle_incoming_message(message, client_address):
    print(f"Received message from {client_address}: {message}")

def main():
    """Main function to run the Authoritative Server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))
    print("Authoritative Server running on port 53533")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Received message from {client_address}")
        response = handle_message(message.decode())
        server_socket.sendto(response.encode(), client_address)


if __name__ == "__main__":
    main()
