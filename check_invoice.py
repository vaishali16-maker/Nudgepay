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
headers = {"Authorization": f"Bearer {token}"}

g = requests.get(f"{base}/v2/invoicing/invoices/{invoice_id}", headers=headers)
data = g.json()
print("status:", data.get("status"))
print("total:", data.get("amount", {}).get("value"))
print("paid:", data.get("due_amount", {}).get("value"), "still due")