from flask import Flask, render_template, jsonify
import json, os

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/devices')
def get_devices():
    if os.path.exists("current_devices.json"):
        with open("current_devices.json") as f:
            devices = json.load(f)
    else:
        devices = []
    return jsonify(devices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)