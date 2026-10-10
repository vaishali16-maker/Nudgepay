import os
import requests
from dotenv import load_dotenv

load_dotenv()
base = os.getenv("PAYPAL_BASE_URL")

# 1. Get an access token
t = requests.post(
    f"{base}/v1/oauth2/token",
    auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_CLIENT_SECRET")),
    data={"grant_type": "client_credentials"},
)
token = t.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 2. Create a draft invoice
body = {
    "detail": {"currency_code": "USD", "note": "Thanks for your business!"},
    "invoicer": {"email_address": os.getenv("PAYPAL_SELLER_EMAIL")},
    "primary_recipients": [
        {"billing_info": {"email_address": os.getenv("PAYPAL_BUYER_EMAIL")}}
    ],
    "items": [
        {
            "name": "Logo design",
            "quantity": "1",
            "unit_amount": {"currency_code": "USD", "value": "800.00"},
        }
    ],
}

r = requests.post(f"{base}/v2/invoicing/invoices", headers=headers, json=body)
print(r.status_code)
print(r.text)