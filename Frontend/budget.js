function showModal() {
    document.getElementById("modal").style.display = "flex";
    loadCategories();
}

function hideModal() {
    document.getElementById("modal").style.display = "none";
}

async function saveBudget() {
    const category_id = document.getElementById("tx-category").value;
    const amount = document.getElementById("tx-amount").value;
    const date = document.getElementById("tx-date").value;

    if(!category_id || !amount || !date){
        showToast("Please fill all the fields!");
        return;
    }

    const token = getToken();

    const budgetData = {
        category_id: parseInt(category_id),
        amount: parseFloat(amount),
        date: date
    };

    try {
        const response = await fetch(`${BASE_URL}/budgets`, {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + getToken(),
                "Content-Type": "application/json"
            },
            body: JSON.stringify(budgetData)
        })
        if (!response.ok) throw new Error("Failed to save");

        hideModal();
        showToast("Budget added!");
        loadBudgets();

    } catch (err) {
        showToast("Failed to save budget", "error");
    }
}

async function loadBudgets() {

    try {

        const response = await fetch(`${BASE_URL}/budgets`, {
            headers: {
                "Authorization": "Bearer " + getToken()
            }
        });

        const budgets = await response.json();
        const budgetList = document.getElementById("budget-list");

        budgetList.innerHTML = "";

        budgets.forEach(budget => {
            const row = document.createElement("div")
            row.className = "budget-row";
            row.innerHTML = `
                <div class="budget-left">
                    <div class="budget-name">
                        ${budget.category.name}
                    </div>
                    <div class="budget-meta">
                        Budget Limit
                    </div>
                </div>

                <div class="budget-right">
                    <div class="budget-amount">
                        ₹${budget.amount}
                    </div>
                    <div class="budget-progress">
                        <div class="progress-fill" style="width:50%;"></div>
                    </div>
                </div>
            `;
            budgetList.appendChild(row);
        });

    } catch (err) {
        console.error(err);
        showToast("Failed to load budgets", "error");
    }
}

window.onload = function () {
    loadUser();
    loadBudgets();
    loadCategories()
};
