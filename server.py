from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Pixeldrain API key
API_KEY = "8bb2e5b3-d481-45fd-9f2f-bdc788754888"

# CORS ayarı (NeoCities’den istek için)
from flask_cors import CORS
CORS(app)

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Dosya bulunamadı"}), 400
    file = request.files['file']

    # Pixeldrain'e upload
    url = "https://pixeldrain.com/api/file"
    files = {"file": (file.filename, file.stream, file.mimetype)}
    try:
        response = requests.post(url, files=files, auth=HTTPBasicAuth("", API_KEY))
        result = response.json()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
