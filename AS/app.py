from flask import Flask, request, jsonify
import socket

app = Flask(__name__)
dns_records = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    dns_records[hostname] = ip
    return jsonify({"status": "Registered"}), 201

@app.route('/query', methods=['GET'])
def query():
    hostname = request.args.get('hostname')
    ip = dns_records.get(hostname)
    if ip:
        return jsonify({"ip": ip}), 200
    return jsonify({"error": "Hostname not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53533)
