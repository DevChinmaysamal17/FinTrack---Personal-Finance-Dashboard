def create_category(client, auth_headers):
    response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "category_type": "expense"
        },
        headers=auth_headers
    )

    return response.json()["id"]


def test_create_transaction(client, auth_headers):
    category_id = create_category(client, auth_headers)

    response = client.post(
        "/transactions/",
        json={
            "amount": 500,
            "type": "expense",
            "note": "Dinner",
            "date": "2026-09-04T16:00:00",
            "category_id": category_id
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["amount"] == 500
    assert data["type"] == "expense"
    assert data["note"] == "Dinner"
    assert data["category_id"] == category_id


def test_get_transactions(client, auth_headers):
    response = client.get(
        "/transactions/",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_transaction(client, auth_headers):
    category_id = create_category(client, auth_headers)

    create_response = client.post(
        "/transactions/",
        json={
            "amount": 500,
            "type": "expense",
            "note": "Dinner",
            "date": "2026-09-04T16:00:00",
            "category_id": category_id
        },
        headers=auth_headers
    )

    transaction_id = create_response.json()["id"]

    response = client.put(
        f"/transactions/{transaction_id}",
        json={
            "amount": 750,
            "type": "expense",
            "note": "Updated Dinner",
            "date": "2026-09-04T16:00:00",
            "category_id": category_id
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["amount"] == 750
    assert data["note"] == "Updated Dinner"


def test_delete_nonexistent_transaction(client, auth_headers):
    response = client.delete(
        "/transactions/999999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"