
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from amount_parser import parse_amount

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
    amount = parse_amount(text)

    is_transfer = (
        "transfer" in text
        or "send money" in text
        or "send " in text
    )

    if text in ["hello", "hi", "hey"]:
        reply = (
            "Hello! Welcome to Voice Banking. "
            "How can I help you today?"
        )

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

    elif is_transfer:
        if amount is None:
            reply = (
                "This demo cannot transfer money. "
                "No real banking transactions can be performed. "
                "You can provide an amount to demonstrate a "
                "transfer request."
            )

        elif " to " not in f" {text} ":
            reply = (
                f"You requested a transfer of ₹{amount:.2f}. "
                "This demo cannot transfer money. "
                "No money has been transferred. "
                "Who is the intended recipient? "
                "For example, say 'Transfer 750 rupees to Ravi'."
            )

        else:
            recipient = text.split(" to ", 1)[1].strip()

            if not recipient:
                reply = (
                    f"You requested a transfer of ₹{amount:.2f}. "
                    "This demo cannot transfer money. "
                    "No money has been transferred. "
                    "Please provide a recipient name for the demo."
                )
            else:
                reply = (
                    f"You requested a transfer of ₹{amount:.2f} "
                    f"to {recipient}. "
                    "This demo cannot transfer money. "
                    "No money has been transferred."
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

    return {
        "reply": reply,
        "detected_amount": amount,
    }
