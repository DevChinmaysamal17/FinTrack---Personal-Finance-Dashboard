const BASE_URL = "";  // Empty because both frontend and backend share same url

function getToken() {
    return localStorage.getItem("token");
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

function formatCurrency(n) {
    return "₹" + Number(n).toLocaleString("en-IN");
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString("en-IN", {
        year: "numeric",
        month: "short",
        day: "numeric"
    });
}

// Shows a small toast message instead of alert()
function showToast(message, type = "success") {
    const existing = document.getElementById("toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.id = "toast";
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: ${type === "error" ? "#e74c3c" : "#2ecc71"};
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        animation: fadeIn 0.2s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// To get username and email on the bottom left
async function loadUser() {
    const token = getToken();
    if (!token) {
        window.location.href = "/";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/me`, {
            headers: { "Authorization": "Bearer " + token }
        });

        if (!response.ok) throw new Error("Unauthorized");

        const user = await response.json();
        document.getElementById("user-name").textContent = user.name;
        document.getElementById("user-email").textContent = user.email;

    } catch (err) {
        console.error(err);
        window.location.href = "/";
    }
}

// To load categories 
async function loadCategories() {
    try {
        const response = await fetch(`${BASE_URL}/categories`, {
            headers: { "Authorization": "Bearer " + getToken() }
        });
        const categories = await response.json();
 
        const select = document.getElementById("tx-category");
        select.innerHTML = '<option value="">Select category</option>';
 
        categories.forEach(cat => {
            const option = document.createElement("option");
            option.value = cat.id;
            option.textContent = cat.name;
            select.appendChild(option);
        });
    } catch (err) {
        showToast("Failed to load categories", "error");
    }
}