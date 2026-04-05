document.addEventListener("DOMContentLoaded", function () {

    console.log("🔥 SYSTEM READY");

    // smooth scroll (safe kahit wala)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {
                target.scrollIntoView({
                    behavior: "smooth"
                });
            }
        });
    });

    // ✅ UNIVERSAL FORM HANDLER (works for dinein, delivery, event)
    const form = document.querySelector("form");

    if (!form) {
        console.warn("⚠️ No form found on this page");
        return;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const btn = form.querySelector("button[type='submit']");
        if (btn) btn.innerText = "Sending...";

        const data = new FormData(form);

        try {
            const res = await fetch("https://abct-backend.onrender.com/webhook", {
                method: "POST",
                body: data
            });

            const result = await res.json();

            console.log("📡 Response:", result);

            if (result.status === "success") {
                alert("✅ Success!");
                form.reset();
            } else {
                alert("❌ Failed");
            }

        } catch (err) {
            console.error("🔥 Error:", err);
            alert("❌ Error connecting server");
        }

        if (btn) btn.innerText = "Submit";
    });

});