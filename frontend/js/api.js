const API_URL = "http://localhost:8081/api/v1";

async function apiFetch(endpoint, options = {}) {

    // Create full API URL
    const fullURL = API_URL + endpoint;

    // Create default headers
    let headers = {
        "Content-Type": "application/json"
    };

    // Get token from localStorage
    const token = localStorage.getItem("access_token");

    // Add token if user is logged in
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    // Send request
    try {

        const response = await fetch(fullURL, {
            ...options,
            headers: {
                ...headers,
                ...(options.headers || {})
            }
        });

        // Handle expired login
        if (response.status === 401 &&
            !endpoint.includes("/auth/login")) {

            localStorage.removeItem("access_token");

            window.location.href =
                "/login.html?expired=true";

            throw new Error(
                "Session expired. Login again."
            );
        }

        return response;

    } catch (error) {

        console.error("API Error:", error);

        throw error;
    }
}