from fastapi import FastAPI
import requests

app = FastAPI()

# Multiple mirror nodes to check
MIRROR_NODES = [
    "https://mainnet-public.mirrornode.hedera.com/api/v1",
    "https://api.kabuto.sh/v1",
    "https://hedera.ledgerworks.io/api/v1"
]

DESTINATION_WALLET = "0.0.8063721"
TOKEN_ID = "0.0.7917527"

@app.get("/")
def home():
    return {"status": "OK", "message": "FastAPI is running!"}

@app.get("/verify_transaction/")
def verify_transaction(wallet_address: str):
    try:
        print(f"Checking transactions for wallet: {wallet_address}")

        for node in MIRROR_NODES:
            print(f"Trying Mirror Node: {node}")

            # Try the account transactions API
            response = requests.get(f"{node}/accounts/{wallet_address}/transactions?order=desc&limit=10")
            if response.status_code == 200:
                data = response.json()
                print(f"API Response from {node}: {data}")

                if "transactions" in data:
                    for tx in data["transactions"]:
                        if "token_transfers" in tx:
                            for transfer in tx["token_transfers"]:
                                if transfer["account"] == DESTINATION_WALLET and transfer["amount"] == 1 and transfer["token_id"] == TOKEN_ID:
                                    return {"status": "verified", "message": f"SLOTH Token Transaction Verified from {node}"}

        return {"status": "not_found", "message": "SLOTH Token transaction not found"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
