import os
from fastapi import FastAPI, Request, HTTPException, Response
from groq import Groq

app = FastAPI()

# Environment variable se key uthayega (yahan key mat likhna)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_secret_123")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

@app.get("/")
def home():
    return {"status": "Universal Creator AI Backend Active"}

@app.get("/webhook")
def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    
    try:
        entry = data.get("entry", [])[0]
        messaging = entry.get("messaging", [])[0]
        sender_id = messaging.get("sender", {}).get("id")
        user_message = messaging.get("message", {}).get("text")

        if user_message and groq_client:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful Instagram sales assistant converting leads naturally."},
                    {"role": "user", "content": user_message}
                ],
                model="llama-3.3-70b-versatile",
            )
            ai_reply = chat_completion.choices[0].message.content
            print(f"AI Response for {sender_id}: {ai_reply}")

    except Exception as e:
        print(f"Error processing webhook: {e}")

    return {"status": "EVENT_RECEIVED"}
