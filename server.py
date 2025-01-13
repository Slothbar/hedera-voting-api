from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Official Hedera Mirror Node
HEDERA_MIRROR_NODE = "https://mainnet-public.mirrornode.hedera.com/api/v1"

DESTINATION_WALLET = "0.0.8063721"  # The wallet receiving the votes
TOKEN_ID = "0.0.7917527"  # SLOTH Token ID

@app.get("/")
def home():
    return {"status": "OK", "message": "FastAPI is running!"}

@app.get("/verify_transaction/")
def verify_transaction(wallet_address: str = Query(..., description="User's Hedera wallet address")):
    try:
        print(f"🔍 Checking transactions for sender wallet: {wallet_address}")

        # Fetch transactions for the user's wallet
        url = f"{HEDERA_MIRROR_NODE}/accounts/{wallet_address}/transactions?order=desc&limit=10"
        response = requests.get(url)
        print(f"➡️ Requesting: {url}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Full API Response: {data}")

            if "transactions" in data and len(data["transactions"]) > 0:
                for tx in data["transactions"]:
                    print(f"🔎 Checking Transaction ID: {tx.get('transaction_id')}")

                    if "token_transfers" in tx:
                        for transfer in tx["token_transfers"]:
                            print(f"🔎 Found Token Transfer - Sender: {wallet_address}, Receiver: {transfer['account']}, Token: {transfer['token_id']}, Amount: {transfer['amount']}")

                            # Check if the transaction was sent to the voting wallet and is exactly 1 SLOTH token
                            if (
                                transfer["account"] == DESTINATION_WALLET
                                and transfer["amount"] == 1
                                and transfer["token_id"] == TOKEN_ID
                            ):
                                return {"status": "verified", "message": "SLOTH Token Transaction Verified"}

            return {"status": "not_found", "message": "SLOTH Token transaction not found"}

        else:
            print(f"⚠️ API Error: {response.status_code} - {response.text}")
            return {"status": "error", "message": response.text}

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {"status": "error", "message": str(e)}
