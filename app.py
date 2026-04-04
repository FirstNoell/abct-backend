from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# 🔐 Load from environment variables
EMAIL_USER = os.getenv("coronadonoell@gmail.com ")
EMAIL_PASS = os.getenv("nsmrwkltqlkossbv")


@app.route("/")
def home():
    return "✅ ABCT Backend is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form.to_dict()

        print("📥 Received booking:", data)

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        booking_type = data.get("booking_type")
        payment_method = data.get("payment_method")
        date = data.get("date")
        time = data.get("time")
        event_type = data.get("event_type")
        guests = data.get("event_guests")

        subject = "📩 New Booking Received"
        body = f"""
New Booking Details:

Name: {name}
Email: {email}
Phone: {phone}
Booking Type: {booking_type}
Payment Method: {payment_method}
Date: {date}
Time: {time}
Event Type: {event_type}
Guests: {guests}
"""

        send_email(subject, body)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500


def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("📧 Email sent successfully!")

    except Exception as e:
        print("❌ Email error:", str(e))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)