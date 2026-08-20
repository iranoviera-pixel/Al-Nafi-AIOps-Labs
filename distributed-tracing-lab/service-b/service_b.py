from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    time.sleep(0.3)
    return jsonify({"message": "Data from Service B"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
