from refund_agent.orders import get_order

order_id = input("Enter order ID: ").strip()
order = get_order(order_id)

if order is None:
    print("Order not found.")
else:
    print(f"Order ID: {order.order_id}")
    print(f"Delivery date: {order.delivery_date}")
    print(f"Item price: ${order.item_price}")
    print(f"Final sale: {order.is_final_sale}")
    print(f"Damaged: {order.is_damaged}")
