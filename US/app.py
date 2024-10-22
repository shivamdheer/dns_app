from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"error": "Missing parameters"}), 400

    response = requests.get(f'http://{as_ip}:{as_port}/query?hostname={hostname}')
    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve FS IP"}), 500
    
    fs_ip = response.json().get("ip")
    if not fs_ip:
        return jsonify({"error": "FS IP not found"}), 404

    fs_url = f'http://{fs_ip}:{fs_port}/fibonacci?number={number}'
    fib_response = requests.get(fs_url)
    return (fib_response.content, fib_response.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
