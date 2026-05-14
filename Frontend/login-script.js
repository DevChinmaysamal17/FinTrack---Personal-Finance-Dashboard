const BASE_URL = "http://127.0.0.1:8000";

// To show register page 
function showRegister() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("register-form").style.display = "block";
}

// To hide register page 
function showLogin() {
    document.getElementById("register-form").style.display = "none";
    document.getElementById("login-form").style.display = "block";
}

// Verification of user credentials with backend
async function login(event) {
    event.preventDefault();

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    if (!email || !password) {
        alert("Enter email and password");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                username: email,
                password: password
            })
        });

        if (!response.ok) throw new Error("Invalid email or password");

        const data = await response.json();

        localStorage.setItem("token", data.access_token);

        window.location.href = "/static/dashboard.html";

    } catch (err) {
        alert(err.message);
    }
}

// To create a new user and saving that data in backend
async function register(event) {
    event.preventDefault();

    const name = document.getElementById("reg-name").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    if (!name || !email || !password) {
        alert("Please fill in all fields");
        return;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json" 
            },
            body: JSON.stringify({
                name: name,
                email: email,    
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Registration failed");
        }

        alert("Account created! Please log in.");
        showLogin();

    } catch (err) {
        alert(err.message);
    }
}

// To get the current user token 
function getToken() {
    return localStorage.getItem("token");
}