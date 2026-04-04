from flask import Flask, request, jsonify
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ==============================
# EMAIL CONFIG (SECURE)
# ==============================
EMAIL_ADDRESS = os.getenv("coronadonoell@gmail.com")
EMAIL_PASSWORD = os.getenv("nsmrwkltqlkossbv")

# ==============================
# HELPERS
# ==============================
def clean_value(value):
    if value is None:
        return ""
    return str(value).strip()

def save_to_csv(data):
    file = "bookings.csv"
    file_exists = False

    try:
        with open(file, "r", encoding="utf-8"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "name",
                "email",
                "phone",
                "booking_type",
                "payment_method",
                "date",
                "time",
                "guests",
                "address",
                "order_details",
                "event_type",
                "event_guests",
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            clean_value(data.get("name")),
            clean_value(data.get("email")),
            clean_value(data.get("phone")),
            clean_value(data.get("booking_type")),
            clean_value(data.get("payment_method")),
            clean_value(data.get("date")),
            clean_value(data.get("time")),
            clean_value(data.get("guests")),
            clean_value(data.get("address")),
            clean_value(data.get("order_details")),
            clean_value(data.get("event_type")),
            clean_value(data.get("event_guests")),
        ])

def build_email_body(data):
    lines = [
        "🍣 New Booking Received:",
        "",
        f"👤 Name: {clean_value(data.get('name'))}",
        f"📧 Email: {clean_value(data.get('email'))}",
        f"📱 Phone: {clean_value(data.get('phone'))}",
        "",
        f"📌 Booking Type: {clean_value(data.get('booking_type'))}",
        f"💳 Payment: {clean_value(data.get('payment_method'))}",
        f"📅 Date: {clean_value(data.get('date'))}",
        f"⏰ Time: {clean_value(data.get('time'))}",
    ]

    booking_type = clean_value(data.get("booking_type"))

    if booking_type == "dine_in":
        guests = clean_value(data.get("guests"))
        if guests:
            lines.extend(["", f"👥 Guests: {guests}"])

    elif booking_type == "delivery":
        address = clean_value(data.get("address"))
        order_details = clean_value(data.get("order_details"))

        if address or order_details:
            lines.append("")
        if address:
            lines.append(f"🏠 Delivery Address: {address}")
        if order_details:
            lines.append(f"🧾 Order Details: {order_details}")

    elif booking_type == "event":
        event_type = clean_value(data.get("event_type"))
        event_guests = clean_value(data.get("event_guests"))

        if event_type or event_guests:
            lines.append("")
        if event_type:
            lines.append(f"🎉 Event Type: {event_type}")
        if event_guests:
            lines.append(f"👥 Event Guests: {event_guests}")

    return "\n".join(lines)

def send_email(data):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("⚠️ Email skipped: missing EMAIL_ADDRESS or EMAIL_PASSWORD")
        return

    subject = "🍣 New Booking - ABCT Restaurant"
    body = build_email_body(data)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("📧 Email sent! ✅")
    except Exception as e:
        print("❌ Email error:", e)

# ==============================
# ROUTES
# ==============================
@app.route("/")
def home():
    return "ABCT backend is running ✅"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "🚀 Webhook is running successfully!"

    # 🔥 FIXED: FormData support
    data = request.form.to_dict()

    print("📥 Received booking:", data)

    save_to_csv(data)
    send_email(data)

    return jsonify({"status": "success"})

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    print("🚀 Starting ABCT Webhook Server...")
    app.run(host="0.0.0.0", port=5000)