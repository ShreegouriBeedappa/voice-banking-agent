
# Voice Banking Agent

A demo voice banking assistant built using React.js and Python FastAPI. It supports English and Hinglish interactions for simulated banking operations.

## Features

- Text-based and voice-based chat.
- English and Hinglish amount recognition.
- Recipient and amount extraction.
- Transfer detail confirmation before proceeding.
- Demo verification code.
- Transfer cancellation.
- Simulated transaction history.
- Balance enquiry response.
- Card support and human support guidance.
- Text-to-speech assistant responses.
- Voice challenge phrase verification.
- Protection against collecting real banking PINs and passwords.
- Demo transfer limit of ₹50,000.

## Technology Stack

**Frontend**
- React.js
- JavaScript
- CSS
- Vite
- Browser Speech Recognition and Speech Synthesis APIs

**Backend**
- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest

## Project Structure

```text
voice-banking-agent/
├── backend/
│   ├── main.py
│   ├── amount_parser.py
│   ├── test_main.py
│   ├── test_amount_parser.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── index.html
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ShreegouriBeedappa/voice-banking-agent.git
cd voice-banking-agent
```

### 2. Start the backend

```bash
cd backend
python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
python -m uvicorn main:app --reload
```

Backend URL: http://127.0.0.1:8000

### 3. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your browser.

## Running Tests

From the backend directory:

```bash
python -m pytest -v
```

## Demo Safety

- This application is a simulated banking demonstration.
- It is not connected to real bank accounts.
- No real money is transferred.
- The demo verification code is `2468`.
- Never enter real banking PINs, passwords, or account credentials.
- The voice challenge is a demonstration only and does not establish speaker identity or detect replayed or synthetic audio.

## Author

Shreegouri Beedappa

GitHub: https://github.com/ShreegouriBeedappa
