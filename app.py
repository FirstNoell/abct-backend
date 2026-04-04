from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import csv

app = Flask(__name__)
CORS(app)

# =========================
# ✅ ENV VARIABLES
# =========================
EMAIL_USER = os.getenv("EMAIL_USER")
DEV_EMAIL = os.getenv("DEV_EMAIL")
STAFF_EMAIL = os.getenv("STAFF_EMAIL")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")


# =========================
# 📩 EMAIL FUNCTION (SAFE + TIMEOUT)
# =========================
def send_email(data):
    try:
        if not RESEND_API_KEY:
            print("❌ Missing RESEND_API_KEY")
            return False

        to_emails = [EMAIL_USER, DEV_EMAIL, STAFF_EMAIL]
        to_emails = [email for email in to_emails if email]

        if not to_emails:
            print("❌ No recipient emails configured")
            return False

        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "ABCT System <onboarding@resend.dev>",
                "to": to_emails,
                "subject": "📩 New Booking - ABCT",
                "html": f"""
                    <h2>New Booking Received</h2>
                    <p><b>Name:</b> {data.get('name')}</p>
                    <p><b>Email:</b> {data.get('email')}</p>
                    <p><b>Phone:</b> {data.get('phone')}</p>
                    <p><b>Booking Type:</b> {data.get('booking_type')}</p>
                    <p><b>Date:</b> {data.get('date')}</p>
                    <p><b>Time:</b> {data.get('time')}</p>
                    <p><b>Guests:</b> {data.get('guests')}</p>
                    <p><b>Address:</b> {data.get('address')}</p>
                    <p><b>Order Details:</b> {data.get('order_details')}</p>
                """
            },
            timeout=10  # 🔥 prevents hanging
        )

        print("📡 Email API status:", response.status_code)
        print("📡 Response:", response.text)

        return response.status_code in [200, 202]

    except Exception as e:
        print("❌ Email error:", str(e))
        return False


# =========================
# 🌐 ROUTES
# =========================
@app.route("/")
def home():
    return "ABCT Backend Running ✅"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form.to_dict()
        print("📥 Received booking:", data)

        # =========================
        # 🔥 SAFE EMAIL (NEVER BREAK SYSTEM)
        # =========================
        try:
            email_sent = send_email(data)
        except Exception as e:
            print("⚠️ Email failed but continuing:", str(e))
            email_sent = False

        # =========================
        # 💾 SAVE TO CSV (ALWAYS WORKS)
        # =========================
        file_exists = os.path.isfile("bookings.csv")

        with open("bookings.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(data)

        return jsonify({
            "status": "success",
            "email_sent": email_sent,
            "message": "Booking saved successfully"
        })

    except Exception as e:
        print("❌ Webhook error:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =========================
# 🚀 RUN (RENDER / LOCAL)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)