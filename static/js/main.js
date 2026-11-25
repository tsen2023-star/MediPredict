
document.addEventListener("DOMContentLoaded", function () {

    // Automatically close alert messages after 5 seconds
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            const closeButton = alert.querySelector(".btn-close");

            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });


    // Smooth scrolling for internal page links
    const internalLinks = document.querySelectorAll('a[href^="#"]');

    internalLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                event.preventDefault();

                targetElement.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        });
    });


    // Add a small visual effect to buttons when clicked
    const buttons = document.querySelectorAll(".btn");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            button.classList.add("button-clicked");

            setTimeout(function () {
                button.classList.remove("button-clicked");
            }, 200);
        });
    });


    // Confirm before submitting logout forms
    const logoutForms = document.querySelectorAll(
        'form[action*="logout"]'
    );

    logoutForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = confirm("Are you sure you want to log out?");

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

});
