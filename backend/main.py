
import re
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from amount_parser import parse_amount


app = FastAPI(title="Voice Banking Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://localhost:{port}"
        for port in range(5173, 5179)
    ] + [
        f"http://127.0.0.1:{port}"
        for port in range(5173, 5179)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


# Demo-only storage. Not connected to a real bank.
pending_transfer = None
mock_transactions = []

DEMO_VERIFICATION_CODE = "2468"
DEMO_TRANSFER_LIMIT = 50000


def extract_recipient(text: str):
    text = text.lower().strip()

    # Remove common Hinglish words before recipient's name
    text = re.sub(
        r"^(?:mujhe|mujhko|main|please)\s+",
        "",
        text
    )

    # English: Send 500 rupees to Rahul
    match = re.search(
        r"\b(?:to|for)\s+([a-z][a-z.'-]*(?:\s+[a-z][a-z.'-]*){0,2})\s*$",
        text,
    )

    if match:
        return match.group(1).strip()

    # Hinglish: Rahul ko 500 rupaye bhejo
    match = re.search(
        r"^([a-z][a-z.'-]*(?:\s+[a-z][a-z.'-]*){0,2})\s+ko\b",
        text,
    )

    if match:
        return match.group(1).strip()

    return None


def is_confirmation(text: str):
    return text.strip().lower() in [
        "yes",
        "yes confirm",
        "confirm",
        "i confirm",
        "haan",
        "han",
        "ha",
        "haan confirm",
        "yes proceed",
        "proceed",
    ]


def is_cancellation(text: str):
    return text.strip().lower() in [
        "no",
        "cancel",
        "cancel transfer",
        "no cancel",
        "nahi",
        "nahin",
        "stop",
    ]


def make_transfer_confirmation(amount, recipient):
    return (
        f"Please verify your transfer details. "
        f"Amount: ₹{amount:.2f}. "
        f"Recipient: {recipient.title()}. "
        "Are both details correct? "
        "Say YES to confirm or NO to cancel. "
        "This is a simulated demo transfer. "
        "No real money will be transferred."
    )


@app.get("/")
def home():
    return {
        "message": "Voice Banking Agent backend is running!"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):
    global pending_transfer

    text = request.message.lower().strip()
    amount = parse_amount(text)

    if not text:
        return {
            "reply": "Please enter or speak a message.",
            "detected_amount": None,
        }

    # Never collect a real banking PIN or password.
    if "pin" in text or "password" in text:
        return {
            "reply": (
                "For your safety, never share your real banking "
                "PIN or password with this demo. No credentials "
                "are collected or stored."
            ),
            "detected_amount": None,
        }

    # Cancellation works at either transfer stage.
    if pending_transfer and is_cancellation(text):
        pending_transfer = None

        return {
            "reply": (
                "Your pending demo transfer has been cancelled. "
                "No money has been transferred."
            ),
            "detected_amount": None,
        }

    # Demo verification stage.
    if pending_transfer and pending_transfer.get("awaiting_code"):
        if text == DEMO_VERIFICATION_CODE:
            transaction = {
                "recipient": pending_transfer["recipient"],
                "amount": pending_transfer["amount"],
                "status": "SIMULATED",
                "time": datetime.now().isoformat(timespec="seconds"),
            }

            mock_transactions.append(transaction)
            pending_transfer = None

            return {
                "reply": (
                    "Demo verification successful! "
                    "Your simulated transfer is complete. "
                    "No real money has been transferred."
                ),
                "receipt": transaction,
                "detected_amount": transaction["amount"],
            }

        return {
            "reply": (
                "That demo verification code is incorrect. "
                "Please try again or type NO to cancel."
            ),
            "detected_amount": pending_transfer["amount"],
        }

    # Confirmation stage.
    if pending_transfer and is_confirmation(text):
        pending_transfer["awaiting_code"] = True

        return {
            "reply": (
                "Transfer confirmation received. "
                "For this demo, enter the demo verification code 2468. "
                "Never enter your real banking PIN."
            ),
            "detected_amount": pending_transfer["amount"],
        }

    # Do not start another transfer while one is pending.
    if pending_transfer:
        return {
            "reply": (
                "You already have a demo transfer awaiting confirmation "
                "or verification. Please complete it or type NO to cancel."
            ),
            "detected_amount": pending_transfer["amount"],
        }

    # Greeting.
    greetings = ["hello", "hi", "hey", "namaste", "namaskar"]

    if (
        text in greetings
        or any(text.startswith(g + " ") for g in greetings)
        or text.startswith(("hello,", "hi,", "hey,"))
    ):
        reply = (
            "Hello! Welcome to Voice Banking. "
            "I can help with balance enquiries, transfers, "
            "transaction history, and card support. "
            "How can I help you today?"
        )

    # Balance enquiry.
    elif "balance" in text:
        reply = (
            "This demo is not connected to a real bank account "
            "and cannot access your real account balance."
        )

    # Transaction history.
    elif "transaction" in text or "history" in text:
        if mock_transactions:
            details = [
                f"₹{item['amount']:.2f} to {item['recipient'].title()}"
                for item in mock_transactions
            ]

            reply = (
                "Your simulated demo transactions: "
                + "; ".join(details)
                + ". These are mock records, not real bank transactions."
            )
        else:
            reply = (
                "There are no simulated transactions yet. "
                "This demo has no access to real bank transactions."
            )

    # Card support.
    elif "card" in text:
        reply = (
            "For card-related help, use your bank's official "
            "app or customer support."
        )

    # Human support.
    elif any(word in text for word in [
        "human",
        "agent",
        "customer support",
        "talk to person",
    ]):
        reply = (
            "Your request for human support has been noted "
            "in this demo. Please contact your bank's official "
            "customer support for real assistance."
        )

    # Transfer request.
    elif any(word in text for word in [
        "transfer",
        "send money",
        "send ",
        "bhej do",
        "bhejdo",
        "bhejo",
        "bhej",
    ]):
        recipient = extract_recipient(text)

        # Check amount.
        if amount is None:
            reply = (
                "I could not identify a valid transfer amount. "
                "Please tell me how much you want to transfer."
            )

        # Check recipient.
        elif not recipient:
            reply = (
                "I cannot transfer money without a valid recipient. "
                "Please provide the recipient's name."
            )

        # Apply demo transfer limit.
        elif amount > DEMO_TRANSFER_LIMIT:
            reply = (
                f"The requested amount is ₹{amount:.2f}. "
                f"The maximum transfer limit for this demo is "
                f"₹{DEMO_TRANSFER_LIMIT:.2f}. "
                "Please enter a smaller amount."
            )

        else:
            pending_transfer = {
                "amount": amount,
                "recipient": recipient,
                "awaiting_code": False,
            }

            reply = make_transfer_confirmation(amount, recipient)

    # General help.
    elif "help" in text:
        reply = (
            "You can ask about balances, transfers, "
            "transactions, card support, or human assistance."
        )

    else:
        reply = (
            "I'm your Voice Banking demo assistant. "
            "You can ask about balances, transfers, "
            "transactions, or card support."
        )

    return {
        "reply": reply,
        "detected_amount": amount,
    }
