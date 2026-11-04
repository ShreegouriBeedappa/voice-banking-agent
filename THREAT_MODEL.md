
# Voice Banking Agent – Threat Model

## 1. Purpose

This document describes potential security risks in the Voice Banking Agent demo and the safeguards implemented or considered.

## 2. Assets to Protect

- Transfer amount and recipient details.
- Simulated transaction records.
- User messages and voice input.
- Demo verification process.

## 3. Potential Threats and Mitigations

| Threat | Risk | Mitigation |
|---|---|---|
| Incorrect speech recognition | Wrong amount or recipient | Read back transfer details and require explicit confirmation |
| Missing recipient or amount | Incomplete transfer request | Ask the user for missing details |
| Unauthorized transfer | Unwanted transaction | Require confirmation and demo verification |
| Incorrect verification code | Unauthorized demo completion | Reject incorrect codes |
| Accidental transfer | User makes a mistake | Allow cancellation before completion |
| PIN or password disclosure | Exposure of sensitive credentials | Warn users never to enter real banking credentials |
| Replay or synthetic voice | Voice challenge could be spoofed | Clearly disclose that the demo does not detect replay or synthetic audio |
| Excessive transfer amount | Unsafe demo transaction | Apply a ₹50,000 demo transfer limit |

## 4. Security Limitations

- The application is not connected to a real bank.
- The verification code is hardcoded for demonstration.
- The demo does not use production-grade authentication.
- Voice challenge matching does not verify speaker identity.
- Replay and synthetic speech detection are not implemented.
- Simulated transaction records are stored in memory.

## 5. Future Improvements

- Secure user authentication and session management.
- Encrypted storage and communication.
- Rate limiting and audit logging.
- Production-grade voice liveness detection.
- Secure, time-limited verification codes.
- Human review for suspicious transactions.

## 6. Safety Statement

This application is intended only for demonstration and evaluation. It must not be used to perform real banking transactions or collect real banking credentials.
