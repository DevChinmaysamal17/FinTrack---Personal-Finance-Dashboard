// transactions.js — depends on utils.js being loaded first

let allTransactions = [];
let deleteId = null;

// ── Modal ─────────────────────────────────────────────────
function showModal() {
    document.getElementById("modal").style.display = "flex";
    document.getElementById("tx-date").value = new Date().toISOString().split("T")[0];
    loadCategories();
}

function hideModal() {
    document.getElementById("modal").style.display = "none";
}

function showConfirm(id) {
    deleteId = id;
    document.getElementById("confirm-modal").style.display = "flex";
}

function hideConfirm() {
    deleteId = null;
    document.getElementById("confirm-modal").style.display = "none";
}

// ── Categories ────────────────────────────────────────────
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

// ── Save transaction ──────────────────────────────────────
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

// ── Delete transaction ────────────────────────────────────
// FIX: was confirmDelete(id) called with no argument from the button
// Now uses the module-level deleteId variable set by showConfirm()
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

// ── Filter ────────────────────────────────────────────────
function applyFilter() {
    const type = document.getElementById("filter-type").value;
    const filtered = type === ""
        ? allTransactions
        : allTransactions.filter(tx => tx.type === type);

    renderTable(filtered);
    renderStats(filtered);
}

// ── Render table ──────────────────────────────────────────
function renderTable(transactions) {
    const tbody = document.getElementById("tx-body");

    if (transactions.length === 0) {
        tbody.innerHTML = '<tr class="empty-row"><td colspan="6">No transactions found.</td></tr>';
        return;
    }

    let html = "";

    transactions.forEach(tx => {
        // FIX: category name now works because backend returns category object
        const cat  = tx.category ? tx.category.name : "—";
        const sign = tx.type === "income" ? "+" : "−";

        // FIX: date is now formatted properly instead of raw ISO string
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

    tbody.innerHTML = html;  // FIX: set once, not += in a loop (avoids repeated reflows)
}

// ── Render stats ──────────────────────────────────────────
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

// ── Load transactions ─────────────────────────────────────
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

//Initializing required functions
window.onload = function () {
    loadUser();
    loadTransactions();
};