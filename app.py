from flask import Flask, request, jsonify

app = Flask(__name__)

# Gelen GPS verilerini tutmak için basit liste
gps_data = []

@app.route("/upload_location", methods=["POST"])
def upload_location():
    data = request.json
    if data:
        gps_data.append(data)
        print("Yeni GPS verisi:", data)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

@app.route("/view_locations", methods=["GET"])
def view_locations():
    # Son 50 koordinatı göster
    return jsonify(gps_data[-50:]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
