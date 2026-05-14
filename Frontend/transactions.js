let allTransactions = [];
let deleteId = null;

// Show add transaction card 
function showModal() {
    document.getElementById("modal").style.display = "flex";
    document.getElementById("tx-date").value = new Date().toISOString().split("T")[0];
    loadCategories();
}

// Hide add transaction card 
function hideModal() {
    document.getElementById("modal").style.display = "none";
}

// Show delete confirmation card 
function showConfirm(id) {
    deleteId = id;
    document.getElementById("confirm-modal").style.display = "flex";
}

// Hide delete confirmation card 
function hideConfirm() {
    deleteId = null;
    document.getElementById("confirm-modal").style.display = "none";
}

// To save a transaction and save it to database
async function saveTransaction() {
    const amount      = document.getElementById("tx-amount").value;
    const type        = document.getElementById("tx-type").value;
    const note        = document.getElementById("tx-note").value;
    const category_id = document.getElementById("tx-category").value;
    const date        = document.getElementById("tx-date").value;

    if (!amount || !category_id || !date) {
        showToast("Please fill in all fields", "error");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/transactions`, {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + getToken(),
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                amount: parseFloat(amount),
                type: type,
                note: note,
                category_id: parseInt(category_id),
                date: date
            })
        });

        if (!response.ok) throw new Error("Failed to save");

        hideModal();
        showToast("Transaction added!");
        loadTransactions();

    } catch (err) {
        showToast("Failed to save transaction", "error");
    }
}

// To detele a transaction and also removing it from the database
async function confirmDelete() {
    if (!deleteId) return;

    try {
        const response = await fetch(`${BASE_URL}/transactions/${deleteId}`, {
            method: "DELETE",
            headers: { "Authorization": "Bearer " + getToken() }
        });

        if (!response.ok) throw new Error("Failed to delete");

        hideConfirm();
        showToast("Transaction deleted!");
        loadTransactions();

    } catch (err) {
        showToast("Failed to delete transaction", "error");
    }
}

// To apply fiter on transactions 
function applyFilter() {
    const type = document.getElementById("filter-type").value;
    const filtered = type === ""
        ? allTransactions
        : allTransactions.filter(tx => tx.type === type);

    renderTable(filtered);
    renderStats(filtered);
}

// To show a new transaction in the table 
function renderTable(transactions) {
    const tbody = document.getElementById("tx-body");

    if (transactions.length === 0) {
        tbody.innerHTML = '<tr class="empty-row"><td colspan="6">No transactions found.</td></tr>';
        return;
    }

    let html = "";

    transactions.forEach(tx => {
        const cat  = tx.category ? tx.category.name : "—";
        const sign = tx.type === "income" ? "+" : "-";
        const date = formatDate(tx.date);

        html += `
            <tr>
                <td>${tx.note || "—"}</td>
                <td>${cat}</td>
                <td><span class="badge ${tx.type}">${tx.type}</span></td>
                <td>${date}</td>
                <td class="amount ${tx.type}">${sign}${formatCurrency(tx.amount)}</td>
                <td><button class="btn-del" onclick="showConfirm(${tx.id})">Delete</button></td>
            </tr>
        `;
    });

    tbody.innerHTML = html; 
}

function renderStats(transactions) {
    let income  = 0;
    let expense = 0;

    transactions.forEach(tx => {
        if (tx.type === "income") income  += tx.amount;
        else                      expense += tx.amount;
    });

    document.getElementById("stat-income").textContent  = formatCurrency(income);
    document.getElementById("stat-expense").textContent = formatCurrency(expense);
    document.getElementById("stat-count").textContent   = transactions.length;
}

// To load all transactions 
async function loadTransactions() {
    if (!getToken()) {
        window.location.href = "/";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/transactions`, {
            headers: { "Authorization": "Bearer " + getToken() }
        });

        if (!response.ok) throw new Error("Unauthorized");

        allTransactions = await response.json();
        renderTable(allTransactions);
        renderStats(allTransactions);

    } catch (err) {
        console.error(err);
        localStorage.removeItem("token");
        window.location.href = "/";
    }
}

// Initializing Functions 
window.onload = function () {
    loadUser();
    loadTransactions();
};