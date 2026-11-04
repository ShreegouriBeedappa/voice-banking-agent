# Voice Banking Agent – Evaluation

## 1. What Was Built
- React chat interface with typed and browser-based voice input.
- Python FastAPI backend.
- English and Hinglish amount and recipient extraction.
- Transfer details are read back for explicit confirmation.
- Simulated transfer verification using a demo code.
- Mock balance and transaction responses.

## 2. Functional Test Results
- Backend automated tests: 13 passed.
- Frontend production build: passed.
- Hinglish amount parsing:
  - "paanch sau" = INR 500.
  - "dedh hazaar" = INR 1,500.

## 3. Voice Evaluation
The requested evaluation using 3 synthetic/cloned, 3 replayed, and 3 genuine live voice clips has not yet been completed. No accuracy results are claimed.

## 4. What Was Cut
- Real bank integration and real money transfers.
- Production-grade authentication and OTP verification.
- Reliable replay and synthetic voice detection.
- Persistent transaction storage.
- Full evaluation using the nine requested voice clips.

## 5. Weakest Design Decision
The voice challenge relies on matching a browser speech-recognition transcript with a displayed phrase. This is only a demonstration feature. It does not prove speaker identity or genuine live speech and may be vulnerable to replay or synthetic audio.

## 6. Safety Limitations
This project is a simulated banking demonstration only. It must not be used for real banking credentials or real money transfers.
