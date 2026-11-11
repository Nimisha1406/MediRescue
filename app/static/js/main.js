document.addEventListener("DOMContentLoaded", function () {

    // 1. Set minimum appointment date
    const appointmentDate = document.querySelector(
        'input[name="appointment_date"]'
    );

    if (appointmentDate) {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, "0");
        const day = String(today.getDate()).padStart(2, "0");

        appointmentDate.min = `${year}-${month}-${day}`;
    }

    // 2. Validate phone numbers
    const phoneInputs = document.querySelectorAll(
        'input[name="phone"]'
    );

    phoneInputs.forEach(function (input) {
        input.addEventListener("input", function () {
            this.value = this.value.replace(/\D/g, "").slice(0, 10);
        });
    });

    // 3. Prevent accidental form resubmission
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            const button = form.querySelector(
                'button[type="submit"]'
            );

            if (button && form.checkValidity()) {
                button.disabled = true;
                button.textContent = "Please wait...";
            }
        });
    });

    // 4. Automatically dismiss success messages
    const alerts = document.querySelectorAll(".alert-success");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (typeof bootstrap !== "undefined") {
                bootstrap.Alert.getOrCreateInstance(alert).close();
            }
        }, 5000);
    });

});