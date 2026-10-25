import json
from pathlib import Path
from langchain_core.tools import tool

DATA_PATH = Path(__file__).parent / "data.json"
with open(DATA_PATH, 'r') as file:
    _orders = json.load(file)

orders = {o["order_id"]: o for o in _orders}


@tool
def lookup_order(order_id: str) -> str:
    """Look up an order by ID and return its details as JSON."""
    order = orders.get(order_id)
    if order is None:
        return json.dumps({"error": f"No order found with ID {order_id}."})
    return json.dumps(order)
