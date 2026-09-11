document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const email =
            document.getElementById("email").value.trim();

        const password =
            document.getElementById("password").value;

        const button =
            document.getElementById("loginButton");

        const message =
            document.getElementById("message");

        button.disabled = true;
        button.textContent = "Logging in...";

        try {

            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {

                message.className = "auth-message auth-error";
                message.textContent =
                    data.message || "Login failed";
                message.style.display = "block";

                button.disabled = false;
                button.textContent = "Login →";

                return;
            }

            // Save JWT
            localStorage.setItem(
                "access_token",
                data.access_token
            );

            // Save user information
            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );

            message.className = "auth-message auth-success";
            message.textContent =
                "Login successful! Redirecting...";
            message.style.display = "block";

            // Redirect according to role
            if (data.user.role === "candidate") {

                window.location.href =
                    "/candidate-dashboard";

            } else if (data.user.role === "employer") {

                window.location.href =
                    "/employer-dashboard";

            } else {

                window.location.href = "/";
            }

        } catch (error) {

            console.error(error);

            message.className = "auth-message auth-error";
            message.textContent =
                "Unable to connect to the server.";
            message.style.display = "block";

            button.disabled = false;
            button.textContent = "Login →";
        }

    });

});