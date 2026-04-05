@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.form

        print("📥 Received data:", data)

        form_type = data.get("form-name")

        # COMMON
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        date = data.get("date")
        time_ = data.get("time")

        # BOOKING
        booking_type = data.get("booking_type")
        guests = data.get("guests")

        # DELIVERY
        address = data.get("address")
        order_details = data.get("order_details")
        payment_method = data.get("payment_method")

        # 📝 SAVE CSV
        with open("bookings.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now(),
                form_type,
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

        # 🔥 GET EMAILS FROM ENV
        OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
        STAFF_EMAIL = os.environ.get("STAFF_EMAIL")

        # 👉 DEFAULT (ikaw)
        to_emails = ["coronadonoell@gmail.com"]

        # 👉 ADD OWNER
        if OWNER_EMAIL:
            to_emails.append(OWNER_EMAIL)

        # 👉 ADD STAFF (optional)
        if STAFF_EMAIL:
            to_emails.append(STAFF_EMAIL)

        # 📧 EMAIL CONTENT
        if form_type == "delivery":
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
            <p><strong>Guests:</strong> {guests}</p>
            """

        # 📡 SEND EMAIL
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

        print("📡 Sent to:", to_emails)

        return jsonify({
            "status": "success",
            "email_status": response.status_code
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500