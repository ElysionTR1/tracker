from flask import Flask, request, jsonify
import os
from datetime import datetime
import base64

app = Flask(__name__)

# Kaydedilecek dizinler
os.makedirs("gps_data", exist_ok=True)
os.makedirs("photos", exist_ok=True)

@app.route("/upload_location", methods=["POST"])
def upload_location():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")
    
    if lat is None or lon is None:
        return jsonify({"status": "error", "message": "lat/lon missing"}), 400
    
    # Dosya adı: timestamp
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    filepath = os.path.join("gps_data", filename)
    
    with open(filepath, "w") as f:
        f.write(f"Latitude: {lat}\nLongitude: {lon}\n")
    
    return jsonify({"status": "success"}), 200

@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    data = request.get_json()
    image_b64 = data.get("image")
    
    if image_b64 is None:
        return jsonify({"status": "error", "message": "image missing"}), 400
    
    # Base64 çöz ve kaydet
    image_bytes = base64.b64decode(image_b64)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    filepath = os.path.join("photos", filename)
    
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
