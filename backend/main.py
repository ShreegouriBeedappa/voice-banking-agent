from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Voice Banking Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Voice Banking Agent backend is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    text = request.message.lower().strip()

    if text in ["hello", "hi", "hey"]:
        reply = "Hello! Welcome to Voice Banking. How can I help you today?"
    elif "balance" in text:
        reply = (
            "I can help with balance enquiries. "
            "This demo is not connected to a real bank account."
        )
    elif "transaction" in text or "history" in text:
            reply = (
        "For transaction history, please use your bank's "
        "official app. This demo has no access to real transactions."
    )
    elif "card" in text:
        reply = (
            "For card-related help, use your bank's official "
            "app or customer support."
        )
    elif "transfer" in text or "send money" in text:
        reply = (
        "I can explain how transfers work, but this demo "
        "cannot transfer money or access bank accounts."
    )
    elif "help" in text:
        reply = (
            "You can ask me about balance enquiries, transfers, "
            "transactions, or card support. This is a demo assistant."
        )
    else:
        reply = (
            "I'm your Voice Banking demo assistant. "
            "You can ask about balances, transfers, transactions, or cards."
        )

    return {"reply": reply}
