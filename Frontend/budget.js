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

    if (!category_id || !amount || !date) {
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

        const token = getToken();

        const budgetResponse = await fetch(`${BASE_URL}/budgets`, {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const txResponse = await fetch(`${BASE_URL}/transactions`, {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        if (!budgetResponse.ok || !txResponse.ok) {
            throw new Error("Failed to fetch data");
        }

        const budgets = await budgetResponse.json();
        const transactions = await txResponse.json();

        const budgetList = document.getElementById("budget-list");

        // TABLE STRUCTURE
        budgetList.innerHTML = `

            <table class="budget-table">

                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Spent</th>
                        <th>Budget</th>
                        <th>Remaining</th>
                        <th>Usage</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody id="budget-table-body">

                </tbody>

            </table>
        `;

        const tableBody = document.getElementById("budget-table-body");

        budgets.forEach(budget => {

            const spent = transactions
                .filter(tx =>
                    tx.type.toLowerCase() === "expense" &&
                    (
                        tx.category_id === budget.category_id ||
                        tx.category?.id === budget.category_id
                    )

)
                .reduce((sum, tx) => sum + tx.amount, 0);

            const percentage = Math.min(
                (spent / budget.amount) * 100,
                100
            );

            const remaining = budget.amount - spent;

            let progressColor = "#22c55e";

            if (percentage > 85) {
                progressColor = "#ef4444";
            }
            else if (percentage > 50) {
                progressColor = "#f59e0b";
            }

            const row = document.createElement("tr");

            row.innerHTML = `

                <td class="category-cell">
                    ${budget.category.name}
                </td>

                <td class="spent-cell">
                    ₹${spent.toFixed(2)}
                </td>

                <td class="budget-cell">
                    ₹${budget.amount.toFixed(2)}
                </td>

                <td class="remaining-cell ${remaining < 0 ? 'danger' : ''}">
                    ₹${remaining.toFixed(2)}
                </td>

                <td>

                    <div class="budget-progress">

                        <div
                            class="progress-fill"
                            style="
                                width:${percentage}%;
                                background:${progressColor};
                            "
                        ></div>

                    </div>

                    <div class="progress-text">
                        ${percentage.toFixed(0)}% Used
                    </div>

                </td>

                <td>

                    <button
                        class="delete-button"
                        onclick="deleteBudget(${budget.id})"
                    >
                        Delete
                    </button>

                </td>
            `;

            tableBody.appendChild(row);
        });

    } catch (err) {

        console.error(err);

        showToast("Failed to load budgets", "error");
    }
}

async function deleteBudget(id) {
    try {
        const response = await fetch(`${BASE_URL}/budgets/${id}`, {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + getToken()
            }
        });


        if (!response.ok) {
            throw new Error("Failed to delete budget");
        }
        showToast("Budget deleted!", "success");
        loadBudgets();

    } catch (err) {
        console.error(err);
        showToast("Failed to delete budget", "error");
    }
}

window.onload = function () {
    loadUser();
    loadBudgets();
    loadCategories()
};
