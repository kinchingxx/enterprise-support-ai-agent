from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_customers():
    response = client.get("/customers")

    assert response.status_code == 200

    customers = response.json()

    assert len(customers) == 100
    assert "customer_id" in customers[0]
    assert "company_name" in customers[0]


def test_get_customer():
    response = client.get("/customers/C0001")

    assert response.status_code == 200
    assert response.json()["customer_id"] == "C0001"


def test_customer_not_found():
    response = client.get("/customers/C9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 10
    assert "product_id" in products[0]


def test_get_tickets():
    response = client.get("/tickets")

    assert response.status_code == 200

    tickets = response.json()

    assert len(tickets) == 1000
    assert "ticket_id" in tickets[0]


def test_filter_critical_tickets():
    response = client.get("/tickets?priority=Critical")

    assert response.status_code == 200

    tickets = response.json()

    assert len(tickets) > 0

    for ticket in tickets:
        assert ticket["priority"] == "Critical"


def test_filter_open_critical_tickets():
    response = client.get(
        "/tickets?status=Open&priority=Critical"
    )

    assert response.status_code == 200

    tickets = response.json()

    for ticket in tickets:
        assert ticket["status"] == "Open"
        assert ticket["priority"] == "Critical"