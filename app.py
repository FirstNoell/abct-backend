from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 🔥 Enable CORS (VERY IMPORTANT)

# ✅ Health check (optional but useful)
@app.route("/", methods=["GET"])
def home():
    return "ABCT Backend is running!"

# ✅ Webhook endpoint (for your form)
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form.to_dict()

        print("📥 Received booking:", data)

        # 👉 pwede mo lagyan ng logic dito (email, save, etc.)

        return jsonify({
            "status": "success",
            "message": "Booking received!"
        })

    except Exception as e:
        print("❌ ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)