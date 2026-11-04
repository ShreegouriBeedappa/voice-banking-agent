
# Voice Banking Agent – Architecture

## 1. Overview

The Voice Banking Agent is a simulated banking assistant that supports typed and voice-based interactions in English and Hinglish.

The application uses a React frontend and a Python FastAPI backend.

## 2. Architecture

```text
User
  |
  v
React Frontend
  |
  | HTTP POST /chat
  v
FastAPI Backend
  |
  +-- Amount Parser
  |
  +-- Recipient Extraction
  |
  +-- Transfer Validation
  |
  +-- Confirmation and Verification
  |
  +-- Mock Transaction Storage
  |
  v
Response to React Frontend
  |
  v
Text and Voice Response
```

## 3. Frontend

- React.js provides the chat interface.
- Browser speech recognition supports voice input.
- Browser speech synthesis provides spoken assistant responses.
- The frontend sends user messages to the backend.

## 4. Backend

- FastAPI exposes the chat API.
- Pydantic validates incoming requests.
- The amount parser recognizes numeric and Hinglish amounts.
- Recipient extraction identifies the intended beneficiary.
- Transfer validation checks the amount and recipient.
- Explicit confirmation is required before demo verification.
- Simulated transactions are stored in application memory.

## 5. Transfer Flow

1. User enters or speaks a transfer request.
2. Backend extracts the amount and recipient.
3. Missing or invalid details are requested.
4. Assistant reads back the transfer details.
5. User confirms or cancels.
6. Demo verification is requested after confirmation.
7. A successful demo verification creates a simulated transaction receipt.

## 6. Safety

- The application is not connected to real banking systems.
- No real money is transferred.
- Real banking PINs and passwords must never be collected.
- A demo verification code is used for testing only.
- The voice challenge is not biometric authentication and does not detect replay or synthetic audio.

## 7. Limitations

- Transactions are stored in memory and are not persistent.
- The application does not connect to real bank accounts.
- Voice challenge matching does not establish speaker identity.
- Production banking authentication and security controls are not implemented.
