document.addEventListener("DOMContentLoaded", function () {

    console.log("JS LOADED");

    const form = document.getElementById("bookingForm");

    if (!form) {
        console.error("❌ bookingForm not found");
        return;
    }

    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch("https://abct-backend.onrender.com/webhook", {
                method: "POST",
                body: formData
            });

            console.log("Response status:", response.status);

            const result = await response.json();
            console.log("Result:", result);

            if (result.status === "success") {
                alert("✅ Booking submitted successfully!");
                form.reset();
            } else {
                alert("❌ Failed: " + JSON.stringify(result));
            }

        } catch (error) {
            console.error("Error:", error);
            alert("❌ Error connecting to server");
        }
    });

});