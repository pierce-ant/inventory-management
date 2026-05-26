"""
Tests for the restocking feature: inventory lead times, the restock-orders
endpoints (GET /api/restock-orders, POST /api/restock-orders), and the
demand-forecast-to-inventory SKU join the Restocking tab relies on.

Note: restock orders live in an in-memory module-level list, so records
created by one test remain visible to later tests in the same session.
Tests therefore never assume the list is empty and always look up the
orders they created by their own order_number.
"""
from datetime import datetime, timedelta

import pytest


def create_sample_restock_payload(client, item_count=2):
    """Build a valid POST payload from real inventory SKUs."""
    response = client.get("/api/inventory")
    assert response.status_code == 200
    inventory = response.json()
    assert len(inventory) >= item_count

    return {
        "budget": 25000,
        "items": [
            {"sku": item["sku"], "quantity": 10 + index}
            for index, item in enumerate(inventory[:item_count])
        ]
    }


class TestInventoryLeadTime:
    """Test suite for the lead_time_days field on inventory items."""

    def test_inventory_items_have_lead_time_days(self, client):
        """Test that every inventory item exposes a lead time in the 5-21 day range."""
        response = client.get("/api/inventory")
        assert response.status_code == 200

        data = response.json()
        assert len(data) > 0

        for item in data:
            assert "lead_time_days" in item
            assert isinstance(item["lead_time_days"], int)
            assert 5 <= item["lead_time_days"] <= 21


class TestRestockOrderEndpoints:
    """Test suite for the restock-orders endpoints."""

    def test_get_restock_orders_returns_list(self, client):
        """Test getting all restock orders returns a list."""
        response = client.get("/api/restock-orders")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    def test_create_restock_order_success(self, client):
        """Test creating a restock order enriches items and derives totals and lead time."""
        payload = create_sample_restock_payload(client)
        inventory = {item["sku"]: item for item in client.get("/api/inventory").json()}

        response = client.post("/api/restock-orders", json=payload)
        assert response.status_code == 201

        order = response.json()
        assert order["order_number"].startswith("RST-")
        assert order["status"] == "Submitted"
        assert order["budget"] == payload["budget"]
        assert len(order["items"]) == len(payload["items"])

        # Items are enriched server-side from inventory
        for line in order["items"]:
            source = inventory[line["sku"]]
            assert line["name"] == source["name"]
            assert abs(line["unit_cost"] - source["unit_cost"]) < 0.01
            assert line["lead_time_days"] == source["lead_time_days"]
            assert abs(line["line_total"] - line["quantity"] * line["unit_cost"]) < 0.01

        # Total cost is the sum of line totals
        calculated_total = sum(line["line_total"] for line in order["items"])
        assert abs(order["total_cost"] - calculated_total) < 0.01

        # Order lead time is the slowest item's lead time
        assert order["lead_time_days"] == max(line["lead_time_days"] for line in order["items"])

        # Dates are ISO 8601 and expected delivery is order date + lead time
        assert "T" in order["order_date"]
        assert "T" in order["expected_delivery"]
        order_date = datetime.fromisoformat(order["order_date"])
        expected_delivery = datetime.fromisoformat(order["expected_delivery"])
        assert expected_delivery - order_date == timedelta(days=order["lead_time_days"])

    def test_created_restock_order_appears_in_list(self, client):
        """Test that a created restock order is returned by the list endpoint."""
        payload = create_sample_restock_payload(client)
        created = client.post("/api/restock-orders", json=payload).json()

        response = client.get("/api/restock-orders")
        assert response.status_code == 200

        order_numbers = [order["order_number"] for order in response.json()]
        assert created["order_number"] in order_numbers

    def test_create_restock_order_empty_items_rejected(self, client):
        """Test that an order with no items is rejected with 400."""
        response = client.post("/api/restock-orders", json={"items": []})
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert "item" in data["detail"].lower()

    def test_create_restock_order_invalid_quantity_rejected(self, client):
        """Test that zero or negative quantities are rejected with 422."""
        for quantity in [0, -5]:
            response = client.post(
                "/api/restock-orders",
                json={"items": [{"sku": "TMP-201", "quantity": quantity}]}
            )
            assert response.status_code == 422

    def test_create_restock_order_unknown_sku_rejected(self, client):
        """Test that an unknown SKU is rejected with 400 and named in the error."""
        response = client.post(
            "/api/restock-orders",
            json={"items": [{"sku": "NOPE-999", "quantity": 5}]}
        )
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert "NOPE-999" in data["detail"]

    def test_restock_orders_unique_order_numbers(self, client):
        """Test that consecutive restock orders get distinct ids and order numbers."""
        payload = create_sample_restock_payload(client, item_count=1)
        first = client.post("/api/restock-orders", json=payload).json()
        second = client.post("/api/restock-orders", json=payload).json()

        assert first["id"] != second["id"]
        assert first["order_number"] != second["order_number"]

    def test_restock_order_does_not_affect_customer_orders_or_dashboard(self, client):
        """Test that submitting a restock order leaves customer orders and dashboard metrics unchanged."""
        orders_before = client.get("/api/orders").json()
        summary_before = client.get("/api/dashboard/summary").json()

        payload = create_sample_restock_payload(client)
        response = client.post("/api/restock-orders", json=payload)
        assert response.status_code == 201

        orders_after = client.get("/api/orders").json()
        summary_after = client.get("/api/dashboard/summary").json()

        assert len(orders_after) == len(orders_before)
        assert summary_after == summary_before


class TestDemandForecastJoin:
    """Test suite guarding the forecast-to-inventory join used for recommendations."""

    def test_forecasts_include_inventory_skus(self, client):
        """Test that enough demand forecasts reference real inventory SKUs."""
        forecasts = client.get("/api/demand").json()
        inventory_skus = {item["sku"] for item in client.get("/api/inventory").json()}

        joinable = [f for f in forecasts if f["item_sku"] in inventory_skus]
        assert len(joinable) >= 6
