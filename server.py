from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup

app = FastAPI()

HASHSCAN_URL = "https://hashscan.io/mainnet/account"

DESTINATION_WALLET = "0.0.8063721"
TOKEN_ID = "0.0.7917527"

@app.get("/")
def home():
    return {"status": "OK", "message": "FastAPI is running!"}

@app.get("/verify_transaction/")
def verify_transaction(wallet_address: str = Query(..., description="User's Hedera wallet address")):
    try:
        print(f"🔍 Checking HashScan for wallet: {wallet_address}")

        # Scrape HashScan
        url = f"{HASHSCAN_URL}/{wallet_address}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract all transaction data
            transactions = soup.find_all("tr")  # Modify this to find transaction tables

            for tx in transactions:
                if TOKEN_ID in tx.text and DESTINATION_WALLET in tx.text:
                    return {"status": "verified", "message": "SLOTH Token Transaction Verified via HashScan"}

            return {"status": "not_found", "message": "SLOTH Token transaction not found on HashScan"}

        else:
            print(f"⚠️ HashScan Error: {response.status_code} - {response.text}")
            return {"status": "error", "message": response.text}

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {"status": "error", "message": str(e)}
