from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    # Step 2: Register with the Authoritative Server
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))

    # Receive response (optional)
    response, _ = sock.recvfrom(1024)

    return jsonify({"status": "Registered"}), 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    try:
        number = int(number)
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400

    # Compute Fibonacci number
    if number < 0:
        return jsonify({"error": "Negative numbers not allowed"}), 400
    a, b = 0, 1
    for _ in range(number):
        a, b = b, a + b
    return jsonify({"fibonacci": a}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
