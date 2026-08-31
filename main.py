import os
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_secret_123")

@app.get("/")
def home():
    return {"status": "Universal Creator AI Active"}

@app.get("/webhook")
def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    raise HTTPException(status_code=403, detail="Verification failed")
