document.getElementById("bookingForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    try {
        const response = await fetch("https://abct-backend.onrender.com/webhook", {
            method: "POST",
            body: formData
        });

        console.log("Response:", response);

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
        alert("❌ Error: " + error.message);
    }
});