from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime
import requests
import os

app = Flask(__name__)
CORS(app)

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form

        print("📥 Received data:", data)

        # COMMON
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        date = data.get("date")

        # 🔥 TIME FIX (24 → 12 FORMAT)
        time_raw = data.get("time")
        if time_raw:
            try:
                time_ = datetime.strptime(time_raw, "%H:%M").strftime("%I:%M %p")
            except:
                time_ = time_raw
        else:
            time_ = None

        # TYPE
        booking_type = data.get("booking_type")

        # OPTIONAL
        guests = data.get("guests")
        address = data.get("address")
        order_details = data.get("order_details")
        payment_method = data.get("payment_method")

        # 📝 SAVE CSV
        with open("bookings.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now(),
                name,
                email,
                phone,
                booking_type,
                guests,
                address,
                order_details,
                payment_method,
                date,
                time_
            ])

        # ❌ API KEY CHECK
        if not RESEND_API_KEY:
            return jsonify({"status": "error", "message": "Missing API key"}), 500

        # 📧 EMAIL TARGETS
        OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
        STAFF_EMAIL = os.environ.get("STAFF_EMAIL")

        to_emails = ["coronadonoell@gmail.com"]

        if OWNER_EMAIL:
            to_emails.append(OWNER_EMAIL)

        if STAFF_EMAIL:
            to_emails.append(STAFF_EMAIL)

        # 🚚 DELIVERY EMAIL
        if booking_type == "delivery":
            subject = "🚚 New Delivery Order"
            html_content = f"""
            <h2>New Delivery Order</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Address:</strong> {address}</p>
            <p><strong>Order:</strong> {order_details}</p>
            <p><strong>Payment:</strong> {payment_method}</p>
            <p><strong>Date:</strong> {date}</p>
            <p><strong>Time:</strong> {time_}</p>
            """

        # 🍽️ DINE-IN / EVENT
        else:
            subject = "📅 New Booking Received"
            html_content = f"""
            <h2>New Booking</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Type:</strong> {booking_type}</p>
            <p><strong>Date:</strong> {date}</p>
            <p><strong>Time:</strong> {time_}</p>
            {"<p><strong>Guests:</strong> " + str(guests) + "</p>" if guests else ""}
            """

        # 📡 SEND EMAIL
        # 📡 SEND EMAIL
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",  # ✅ FIXED
                "to": ["coronadonoell@gmail.com"],  # test muna
                "subject": subject,
                "html": html_content
            }
        )

        # 🔍 DEBUG
        print("📡 Status:", response.status_code)
        print("📡 Body:", response.text)

        print("📡 Sent to:", to_emails)

        return jsonify({
            "status": "success",
            "email_status": response.status_code
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
