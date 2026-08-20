from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/trigger')
def trigger():
    response = requests.get('http://service-b:5001/api/data')
    return jsonify({
        "message": "Service A received:",
        "from_service_b": response.json()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
