@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form

        print("📥 Received data:", data)

        # COMMON
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        time_ = data.get("time")

        # TYPE (IMPORTANT)
        booking_type = data.get("booking_type")

        # DINE-IN
        date = data.get("date")
        guests = data.get("guests")

        # DELIVERY
        address = data.get("address")
        order_details = data.get("order_details")
        payment_method = data.get("payment_method")

        # 📝 SAVE CSV (keep everything for records)
        with open("bookings.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now(),
                booking_type,
                name,
                email,
                phone,
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

        # 📧 EMAIL LIST
        OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
        STAFF_EMAIL = os.environ.get("STAFF_EMAIL")

        to_emails = ["coronadonoell@gmail.com"]

        if OWNER_EMAIL:
            to_emails.append(OWNER_EMAIL)

        if STAFF_EMAIL:
            to_emails.append(STAFF_EMAIL)

        # 📧 EMAIL CONTENT (FIXED)
        if booking_type == "delivery":

            subject = "🚚 New Delivery Order"

            html_content = f"""
            <h2>🚚 Delivery Order</h2>

            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone}</p>

            <p><strong>Address:</strong> {address}</p>
            <p><strong>Order:</strong> {order_details or 'N/A'}</p>
            <p><strong>Payment:</strong> {payment_method}</p>

            <p><strong>Time:</strong> {time_ or 'ASAP'}</p>
            """

        else:

            subject = "📅 New Booking Received"

            html_content = f"""
            <h2>🍽️ Dine-in Reservation</h2>

            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone}</p>

            <p><strong>Date:</strong> {date or 'N/A'}</p>
            <p><strong>Time:</strong> {time_ or 'N/A'}</p>
            <p><strong>Guests:</strong> {guests or 'N/A'}</p>
            """

        # 📡 SEND EMAIL (FAIL SAFE)
        try:
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

            print("📡 Email status:", response.status_code)

        except Exception as email_error:
            print("❌ Email failed:", email_error)

        # ALWAYS SUCCESS (IMPORTANT)
        return jsonify({
            "status": "success"
        })

    except Exception as e:
        print("🔥 SERVER ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500