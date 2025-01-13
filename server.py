from fastapi import FastAPI
import requests

app = FastAPI()

HEDERA_API_URL = "https://mainnet-public.mirrornode.hedera.com/api/v1/transactions"
DESTINATION_WALLET = "0.0.8063721"  # Wallet that receives the SLOTH token
TOKEN_ID = "0.0.7917527"  # Your actual SLOTH Token ID

@app.get("/")
def home():
    return {"status": "OK", "message": "FastAPI is running!"}

@app.get("/verify_transaction/")
def verify_transaction(wallet_address: str):
    try:
        response = requests.get(f"{HEDERA_API_URL}?account.id={wallet_address}&order=desc&limit=10")
        data = response.json()

        if "transactions" not in data or not data["transactions"]:
            return {"status": "not_found", "message": "No transactions found"}

        for tx in data["transactions"]:
            if "token_transfers" in tx:
                for transfer in tx["token_transfers"]:
                    if transfer["account"] == DESTINATION_WALLET and transfer["amount"] == 1 and transfer["token_id"] == TOKEN_ID:
                        return {"status": "verified", "message": "SLOTH Token Transaction Verified"}

        return {"status": "not_found", "message": "SLOTH Token transaction not found"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
