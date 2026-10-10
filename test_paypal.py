import os
import requests
from dotenv import load_dotenv

load_dotenv()
base = os.getenv("PAYPAL_BASE_URL")

r = requests.post(
    f"{base}/v1/oauth2/token",
    auth=(os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_CLIENT_SECRET")),
    data={"grant_type": "client_credentials"},
)

print(r.status_code)
print("Token received!" if r.ok else r.text)
