from refund_agent_ref.tools import lookup_order

# Test the tool directly
result = lookup_order.invoke({"order_id": "4821"})
print(result)
