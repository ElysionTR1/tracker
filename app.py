from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
import base64

app = Flask(__name__)

# GPS verilerini geçici tutmak için liste
gps_data = []

# Kaydedilecek dizinler
os.makedirs("gps_data", exist_ok=True)
os.makedirs("photos", exist_ok=True)

# ----------------- GPS Upload -----------------
@app.route("/upload_location", methods=["POST"])
def upload_location():
    data = request.get_json()
    if not data or "latitude" not in data or "longitude" not in data:
        return jsonify({"status": "error", "message": "latitude/longitude missing"}), 400

    lat = data["latitude"]
    lon = data["longitude"]

    # Listeye ekle (harita için)
    gps_data.append({"lat": lat, "lon": lon})

    # Dosyaya kaydet
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    filepath = os.path.join("gps_data", filename)
    with open(filepath, "w") as f:
        f.write(f"Latitude: {lat}\nLongitude: {lon}\n")

    print("Yeni GPS verisi:", data)
    return jsonify({"status": "success"}), 200

# ----------------- Photo Upload -----------------
@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"status": "error", "message": "image missing"}), 400

    image_b64 = data["image"]
    image_bytes = base64.b64decode(image_b64)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    filepath = os.path.join("photos", filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    print(f"Yeni fotoğraf kaydedildi: {filename}")
    return jsonify({"status": "success"}), 200

# ----------------- Harita JSON -----------------
@app.route("/view_locations", methods=["GET"])
def view_locations():
    # Son 50 koordinatı gönder
    return jsonify(gps_data[-50:]), 200

# ----------------- Harita Arayüzü -----------------
@app.route("/")
def index():
    return render_template("index.html")

# ----------------- Uygulamayı Çalıştır -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
