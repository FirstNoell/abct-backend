document.addEventListener("DOMContentLoaded", function () {

    console.log("🔥 JS LOADED");

    const form = document.getElementById("bookingForm");
    const btn = document.getElementById("submitBtn");

    if (!form) {
        console.error("❌ bookingForm NOT FOUND");
        return;
    }

    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        console.log("🚀 Form submitted");

        const formData = new FormData(form);

        try {
            // 🔥 UX improvement (loading state)
            btn.disabled = true;
            btn.innerText = "Processing...";

            console.log("👉 Sending request...");

            const response = await fetch("https://abct-backend.onrender.com/webhook", {
                method: "POST",
                body: formData
            });

            console.log("📡 Response status:", response.status);

            const result = await response.json();
            console.log("📦 Result:", result);

            if (result.status === "success") {
                alert("✅ Booking submitted successfully!");
                form.reset();
            } else {
                alert("❌ Failed: " + JSON.stringify(result));
            }

        } catch (error) {
            console.error("❌ FETCH ERROR:", error);
            alert("❌ Error connecting to server");
        } finally {
            // 🔥 Reset button state
            btn.disabled = false;
            btn.innerText = "Book Now";
        }
    });

});