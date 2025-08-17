from flask import Flask, request, jsonify, render_template_string
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

API_KEY = "8bb2e5b3-d481-45fd-9f2f-bdc788754888"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Pixeldrain Video Yükle</title>
<style>
body { font-family:sans-serif; background:#121212; color:#fff; padding:20px; }
input, button { padding:10px; margin:5px 0; }
button { cursor:pointer; background:#4da3ff; color:#fff; border:none; border-radius:6px; }
#link a { color:#4da3ff; }
</style>
</head>
<body>
<h1>🎬 Pixeldrain Video Yükle</h1>
<input type="file" id="fileInput" accept="video/*">
<button onclick="upload()">Yükle</button>
<p id="status"></p>
<div id="link"></div>

<script>
async function upload() {
  const file = document.getElementById("fileInput").files[0];
  if (!file) return alert("Lütfen bir video seçin!");

  document.getElementById("status").innerText = "Yükleniyor...";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/upload", { method:"POST", body:formData });
    const data = await res.json();

    if(data.id){
      document.getElementById("status").innerText = "Yüklendi ✅";
      document.getElementById("link").innerHTML = `
        <p><a href="https://pixeldrain.com/u/${data.id}" target="_blank">Görüntüleme Linki</a></p>
        <p><a href="https://pixeldrain.com/api/file/${data.id}" target="_blank">Direkt İndirme Linki</a></p>
      `;
    } else {
      document.getElementById("status").innerText = "Hata: " + JSON.stringify(data);
    }
  } catch(err) {
    document.getElementById("status").innerText = "Hata: " + err;
  }
}
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error":"Dosya bulunamadı"}), 400
    file = request.files['file']

    try:
        url = "https://pixeldrain.com/api/file"
        files = {"file": (file.filename, file.stream, file.mimetype)}
        response = requests.post(url, files=files, auth=HTTPBasicAuth("", API_KEY))
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
