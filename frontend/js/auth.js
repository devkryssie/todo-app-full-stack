
document.addEventListener("DOMContentLoaded", function () {

    
    const urlParams = new URLSearchParams(window.location.search);

    
    if (urlParams.has("expired")) {
        showError("Session expired. Please log in again.");
    }

    
    handleRegister(urlParams);

    // Handle Login Form
    handleLogin(urlParams);

});



function handleRegister() {

    const registerForm = document.getElementById("register-form");

    if (!registerForm) return;

    registerForm.addEventListener("submit", async function (event) {

        event.preventDefault();
        clearAlerts();

        
        const firstName = document.getElementById("first_name").value.trim();
        const lastName = document.getElementById("last_name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        
        if (!firstName || !lastName || !email || !password) {
            showError("All fields are required.");
            return;
        }

        if (password.length < 8) {
            showError("Password must be at least 8 characters.");
            return;
        }

        try {

            const response = await apiFetch("/auth/register", {
                method: "POST",
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    password: password
                })
            });

            if (response.status === 201) {
                window.location.href = "/login.html?registered=true";
                return;
            }

            if (response.status === 409) {
                showError("Email already exists.");
                return;
            }

            const data = await response.json();
            showError(data.detail || "Registration failed.");

        } catch (error) {
            showError("Network error.");
        }

    });
}


// ================= LOGIN =================
function handleLogin(urlParams) {

    const loginForm = document.getElementById("login-form");

    if (!loginForm) return;

    // Success message after registration
    if (urlParams.has("registered")) {
        showSuccess("Registration successful! Please log in.");
    }

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();
        clearAlerts();

        // Get values
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        // Validation
        if (!email || !password) {
            showError("All fields are required.");
            return;
        }

        try {

            const response = await apiFetch("/auth/login", {
                method: "POST",
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            if (response.status === 200) {

                const data = await response.json();

                // Save token
                localStorage.setItem(
                    "access_token",
                    data.access_token
                );

                // Go to dashboard
                window.location.href = "/dashboard.html";
                return;
            }

            if (response.status === 401) {
                showError("Wrong email or password.");
                return;
            }

            const data = await response.json();
            showError(data.detail || "Login failed.");

        } catch (error) {
            showError("Network error.");
        }

    });
}


// ================= ALERTS =================
function showError(message) {

    const errorBox = document.getElementById("alert-error");

    if (errorBox) {
        errorBox.textContent = message;
        errorBox.classList.remove("hidden");
    }
}

function showSuccess(message) {

    const successBox = document.getElementById("alert-success");

    if (successBox) {
        successBox.textContent = message;
        successBox.classList.remove("hidden");
    }
}

function clearAlerts() {

    const errorBox = document.getElementById("alert-error");
    const successBox = document.getElementById("alert-success");

    if (errorBox) {
        errorBox.classList.add("hidden");
    }

    if (successBox) {
        successBox.classList.add("hidden");
    }
}


// ================= LOGOUT =================
function logout() {

    // Remove saved token
    localStorage.removeItem("access_token");

    // Return to home page
    window.location.href = "/index.html";
}