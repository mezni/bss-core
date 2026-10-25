import json

from langchain_core.tools import tool

ORDERS: dict[str, dict[str, object]] = {
    "4821": {
        "order_id": "4821",
        "item": "Wireless Headphones",
        "amount_usd": 89.99,
        "days_since_purchase": 12,
        "digital": False,
        "condition": "damaged on arrival",
    },
    "4822": {
        "order_id": "4822",
        "item": "Python Crash Course (ebook)",
        "amount_usd": 29.99,
        "days_since_purchase": 3,
        "digital": True,
        "condition": "downloaded",
    },
    "4823": {
        "order_id": "4823",
        "item": "Standing Desk",
        "amount_usd": 349.00,
        "days_since_purchase": 45,
        "digital": False,
        "condition": "used",
    },
}


@tool
def lookup_order(order_id: str) -> str:
    """Look up an order by ID and return its details as JSON."""
    order = ORDERS.get(order_id)
    if order is None:
        return json.dumps({"error": f"No order found with ID {order_id}."})
    return json.dumps(order)
