import os
from paypal_client import create_invoice, send_invoice, get_invoice

invoice_id = create_invoice(os.getenv("PAYPAL_BUYER_EMAIL"), "Website redesign", 450, due_days=5)
print("created:", invoice_id)
send_invoice(invoice_id)
inv = get_invoice(invoice_id)
print("status:", inv["status"])
print("due date:", inv["detail"]["payment_term"]["due_date"])