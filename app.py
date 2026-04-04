from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)  # 🔥 allow frontend (Vercel) to connect


# =========================
# 📩 EMAIL FUNCTION
# =========================
def send_email(data):
    sender = "coronadonoell@gmail.com"
    password = ": nsmrwkltqlkossbv"

    # 🔥 TEAM EMAILS (OWNER + STAFF + YOU)
    recipients = [
        "charlie0315coronado@email.com",
        # "staff@email.com",
        "coronadonoell@gmail.com"
    ]

    message = f"""
🔥 NEW BOOKING ALERT

Customer Name: {data.get('name')}
Email: {data.get('email')}
Phone: {data.get('phone')}

📅 Date: {data.get('date')}
⏰ Time: {data.get('time')}
👥 Guests: {data.get('guests')}
🍽 Booking Type: {data.get('booking_type')}

------------------------
⚠ ACTION REQUIRED:
Please contact the customer to confirm the booking.
"""

    msg = MIMEText(message)
    msg["Subject"] = "📌 New Booking - ABCT"
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())


# =========================
# 🏠 HEALTH CHECK
# =========================
@app.route("/", methods=["GET"])
def home():
    return "✅ ABCT Backend is running!"


# =========================
# 📥 WEBHOOK (FORM RECEIVER)
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form.to_dict()

        print("📥 Booking received:", data)

        # 🔥 SEND EMAIL TO TEAM
        send_email(data)

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


# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)