from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# ===== ENV VARIABLES =====
EMAIL_USER = os.getenv("EMAIL_USER")  # actual email
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# ===== EMAIL VIA RESEND API =====
def send_email(data):
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {os.environ.get('RESEND_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "from": "ABCT System <onboarding@resend.dev>",
                "to": [
                    os.environ.get("charlie0315coronado@gmail.com"),      # Owner
                    os.environ.get("coronadonoell@gmail.com"),       # Developer
                    os.environ.get("analyn23zamora@gmail.com")      # Inbound/Outbound Staff
                ],
                "subject": "📩 New Booking - ABCT",
                "html": f"""
                    <h2>New Booking</h2>
                    <p><b>Name:</b> {data.get('name')}</p>
                    <p><b>Email:</b> {data.get('email')}</p>
                    <p><b>Phone:</b> {data.get('phone')}</p>
                    <p><b>Date:</b> {data.get('date')}</p>
                    <p><b>Time:</b> {data.get('time')}</p>
                    <p><b>Guests:</b> {data.get('guests')}</p>
                    <p><b>Address:</b> {data.get('address')}</p>
                    <p><b>Order Details:</b> {data.get('order_details')}</p>
                """
            }
        )
        print("✅ Email sent to 3 recipients:", response.status_code)
    except Exception as e:
        print("❌ Email error:", str(e))
# ===== ROUTES =====
@app.route("/")
def home():
    return "ABCT Backend Running ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form.to_dict()
        print("📥 Received booking:", data)

        send_email(data)

        # save to CSV as backup
        import csv
        file_exists = os.path.isfile("bookings.csv")
        with open("bookings.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        return jsonify({"status": "success", "message": "Booking received"})

    except Exception as e:
        print("❌ Webhook error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

# ===== RUN LOCAL =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)