import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()
base = os.getenv("PAYPAL_BASE_URL")
invoice_id = sys.argv[1]

t = requests.post(
    f"{base}/v1/oauth2/token",
    auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_CLIENT_SECRET")),
    data={"grant_type": "client_credentials"},
)
token = t.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Send the invoice to the buyer
s = requests.post(
    f"{base}/v2/invoicing/invoices/{invoice_id}/send",
    headers=headers,
    json={"send_to_recipient": True, "send_to_invoicer": False},
)
print("send:", s.status_code)
print(s.text)

# Check the invoice status
g = requests.get(f"{base}/v2/invoicing/invoices/{invoice_id}", headers=headers)
print("status:", g.json().get("status"))