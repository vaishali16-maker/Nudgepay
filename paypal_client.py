import os
import time
from datetime import date, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv("PAYPAL_BASE_URL")
_token = {"value": None, "expires": 0}


def get_token():
    if _token["value"] and time.time() < _token["expires"]:
        return _token["value"]
    r = requests.post(
        f"{BASE}/v1/oauth2/token",
        auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_CLIENT_SECRET")),
        data={"grant_type": "client_credentials"},
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    _token["value"] = data["access_token"]
    _token["expires"] = time.time() + data["expires_in"] - 60
    return _token["value"]


def _headers():
    return {"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"}


def create_invoice(client_email, description, amount, due_days=7, currency="USD"):
    due = (date.today() + timedelta(days=due_days)).isoformat()
    body = {
        "detail": {
            "currency_code": currency,
            "note": "Thanks for your business!",
            "payment_term": {"term_type": "DUE_ON_DATE_SPECIFIED", "due_date": due},
        },
        "invoicer": {"email_address": os.getenv("PAYPAL_SELLER_EMAIL")},
        "primary_recipients": [{"billing_info": {"email_address": client_email}}],
        "items": [
            {
                "name": description,
                "quantity": "1",
                "unit_amount": {"currency_code": currency, "value": f"{float(amount):.2f}"},
            }
        ],
    }
    r = requests.post(f"{BASE}/v2/invoicing/invoices", headers=_headers(), json=body, timeout=20)
    r.raise_for_status()
    return r.json()["href"].split("/")[-1]


def send_invoice(invoice_id):
    r = requests.post(
        f"{BASE}/v2/invoicing/invoices/{invoice_id}/send",
        headers=_headers(),
        json={"send_to_recipient": True, "send_to_invoicer": False},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()


def get_invoice(invoice_id):
    r = requests.get(f"{BASE}/v2/invoicing/invoices/{invoice_id}", headers=_headers(), timeout=20)
    r.raise_for_status()
    return r.json()