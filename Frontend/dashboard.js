function showModal() {
    document.getElementById("modal").style.display = "flex";
    document.getElementById("tx-date").value =
        new Date().toISOString().split("T")[0];

    loadCategories();
}

function hideModal() {
    document.getElementById("modal").style.display = "none";
}

// Save transaction:
async function saveTransaction() {
    const amount      = document.getElementById("tx-amount").value;
    const type        = document.getElementById("tx-type").value;
    const note        = document.getElementById("tx-note").value;
    const category_id = document.getElementById("tx-category").value;
    const date        = document.getElementById("tx-date").value;

    if (!amount || !category_id) {
        showToast("Enter amount and category", "error");
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
                category_id: parseInt(category_id),
                date: date,
                note: note
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

// Load transactions:
async function loadTransactions() {
    try {
        const response = await fetch(`${BASE_URL}/transactions`, {
            headers: { "Authorization": "Bearer " + getToken() }
        });

        if (!response.ok) throw new Error("Unauthorized");
        const transactions = await response.json();

        let total_income  = 0;
        let total_expense = 0;

        transactions.forEach(tx => {
            if (tx.type === "income") total_income  += tx.amount;
            else total_expense += tx.amount;
        });

        const total_balance = total_income - total_expense;
        const saving_rate   = total_income > 0
            ? ((total_balance / total_income) * 100).toFixed(1):0;

        document.getElementById("card-income").textContent  = formatCurrency(total_income);
        document.getElementById("card-expense").textContent = formatCurrency(total_expense);
        document.getElementById("card-balance").textContent = formatCurrency(total_balance);
        document.getElementById("card-savings").textContent = saving_rate + "%";

        const txList = document.getElementById("tx-list");

        if (!transactions.length) {
            txList.innerHTML = '<div class="empty-msg">No transactions yet.</div>';
            return;
        }

        let html = "";

        transactions.slice(0, 10).forEach(tx => {
            const sign = tx.type === "income" ? "+" : "-";
            const date = formatDate(tx.date);

            html += `
                <div class="tx-row">
                    <div>
                        <div class="tx-name">${tx.note || "Transaction"}</div>
                        <div class="tx-meta">${date}</div>
                    </div>
                    <div class="tx-amount ${tx.type}">
                        ${sign}${formatCurrency(tx.amount)}
                    </div>
                </div>
            `;
        });

        txList.innerHTML = html; 

    } catch (err) {
        console.error(err);
        window.location.href = "/";
    }
}

// Initialize required functions
window.onload = function () {
    loadUser();
    loadTransactions();
};
