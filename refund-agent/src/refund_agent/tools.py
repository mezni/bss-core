from langchain.tools import tool

from refund_agent.orders import get_order


@tool
def lookup_order(order_id: str) -> str:
    """Retrieve order details using an exact order ID.

    Use this tool when a customer asks about an order or refund.
    Never invent an order ID.
    """
    order = get_order(order_id)

    if order is None:
        return f"Order {order_id} was not found."

    return (
        f"Order ID: {order.order_id}\n"
        f"Delivery date: {order.delivery_date}\n"
        f"Item price: {order.item_price}\n"
        f"Final sale: {order.is_final_sale}\n"
        f"Damaged: {order.is_damaged}\n"
        f"Return received: {order.return_received}"
    )
