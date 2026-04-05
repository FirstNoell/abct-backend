document.addEventListener("DOMContentLoaded", function () {

    console.log("🔥 SYSTEM READY");

    // smooth scroll
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

    // form handler
    handleForm("bookingForm", "submitBtn");
    handleForm("deliveryForm", "deliveryBtn");

    function handleForm(formId, btnId) {

        const form = document.getElementById(formId);
        const btn = document.getElementById(btnId);

        if (!form) return;

        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            const data = new FormData(form);

            if (btn) btn.innerText = "Sending...";

            try {
                const res = await fetch("https://abct-backend.onrender.com/webhook", {
                    method: "POST",
                    body: data
                });

                const result = await res.json();

                if (result.status === "success") {
                    alert("Success!");
                    form.reset();
                } else {
                    alert("Failed");
                }

            } catch (err) {
                alert("Error connecting server");
            }

            if (btn) btn.innerText = "Submit";
        });
    }

});