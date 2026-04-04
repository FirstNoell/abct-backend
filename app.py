from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
CORS(app)  # allow requests from your frontend (fixes CORS)

# ===== CONFIG (via Render Environment Variables) =====
EMAIL_USER = os.getenv("coronadonoell@gmail.com")            # your gmail
EMAIL_PASS = os.getenv("vtomdwobxeysvebn")            # app password (16 chars, no spaces)
OWNER_EMAIL = os.getenv("charlie0315coronado") or EMAIL_USER
DEV_EMAIL = os.getenv("coronadonoell") or EMAIL_USER

# ===== EMAIL SENDER =====
def send_email(data):
    try:
        body = f"""
New Booking Received:

Name: {data.get('name')}
Email: {data.get('email')}
Phone: {data.get('phone')}
Booking Type: {data.get('booking_type')}
Date: {data.get('date')}
Time: {data.get('time')}
Guests: {data.get('guests')}
Address: {data.get('address')}
Details: {data.get('order_details')}
"""

        msg = MIMEText(body)
        msg['Subject'] = '📩 New Booking - ABCT'
        msg['From'] = EMAIL_USER
        # send to both owner and dev
        msg['To'] = f"{OWNER_EMAIL}, {DEV_EMAIL}"

        # allow replying directly to the customer's email
        if data.get('email'):
            msg['Reply-To'] = data.get('email')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print("✅ Email sent")

    except Exception as e:
        print("❌ Email error:", str(e))
        raise


# ===== ROUTES =====
@app.route("/")
def home():
    return "ABCT Backend Running ✅"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form
        print("📥 Received booking:", data)

        send_email(data)

        return jsonify({
            "status": "success",
            "message": "Booking received"
        })

    except Exception as e:
        print("❌ Webhook error:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ===== RUN (for local only) =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)