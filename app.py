from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 🔐 ENV VARIABLES
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

@app.route("/")
def home():
    return "ABCT Backend Running 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form

        # 📥 Extract form data
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        booking_type = data.get("booking_type")
        date = data.get("date")
        time_ = data.get("time")
        guests = data.get("guests")

        print("📥 Received booking:", data)

        # 📝 Save to CSV
        with open("bookings.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now(),
                name,
                email,
                phone,
                booking_type,
                date,
                time_,
                guests
            ])

        # ❌ If no API key
        if not RESEND_API_KEY:
            print("❌ Missing RESEND_API_KEY")
            return jsonify({"status": "error", "message": "Missing API key"}), 500

        # 🔥 DEMO MODE → FORCE EMAIL TO YOU
        to_emails = ["coronadonoell@gmail.com"]

        # 📧 Email content
        subject = "📅 New Booking Received"
        html_content = f"""
        <h2>New Booking</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Type:</strong> {booking_type}</p>
        <p><strong>Date:</strong> {date}</p>
        <p><strong>Time:</strong> {time_}</p>
        <p><strong>Guests:</strong> {guests}</p>
        """

        # 📡 Send email via Resend
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "ABCT Booking <onboarding@resend.dev>",
                "to": to_emails,
                "subject": subject,
                "html": html_content
            }
        )

        print("📡 Email API status:", response.status_code)
        print("📡 Response:", response.text)

        return jsonify({
            "status": "success",
            "message": "Booking received",
            "email_status": response.status_code
        })

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)