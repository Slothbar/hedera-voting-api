from fastapi import FastAPI
import requests

app = FastAPI()

# Official Hedera Mirror Node
HEDERA_MIRROR_NODE = "https://mainnet-public.mirrornode.hedera.com/api/v1"

DESTINATION_WALLET = "0.0.8063721"
TOKEN_ID = "0.0.7917527"

@app.get("/")
def home():
    return {"status": "OK", "message": "FastAPI is running!"}

@app.get("/verify_transaction/")
def verify_transaction(wallet_address: str):
    try:
        print(f"🔍 Checking token transfers for wallet: {wallet_address}")

        # Fetch token transfer transactions
        url = f"{HEDERA_MIRROR_NODE}/token-transfers?account.id={wallet_address}&order=desc&limit=10"
        response = requests.get(url)
        print(f"➡️ Requesting: {url}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {data}")

            if "transactions" in data:
                for tx in data["transactions"]:
                    for transfer in tx["token_transfers"]:
                        if (
                            transfer["account"] == DESTINATION_WALLET
                            and transfer["amount"] == 1
                            and transfer["token_id"] == TOKEN_ID
                        ):
                            return {"status": "verified", "message": "SLOTH Token Transaction Verified"}

        return {"status": "not_found", "message": "SLOTH Token transaction not found"}

    except Exception as e:
