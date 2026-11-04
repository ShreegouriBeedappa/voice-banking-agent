# Voice Banking Agent - Demo Script

## Demo Setup

1. Open the project folder in VS Code.
2. Start the backend:
   ```powershell
   cd backend
   .\venv\Scripts\python.exe -m uvicorn main:app --reload
   ```
3. Open a second terminal and start the frontend:
   ```powershell
   cd frontend
   npm run dev
   ```
4. Open the local URL shown by Vite in your browser.

## Demo Steps

1. **Greeting:** Send "Hello" and verify that the assistant responds.
2. **Balance query:** Ask "What is my balance?" and verify the demo balance response.
3. **English transfer:** Enter "I want to transfer 1000 rupees to Priya." Verify that the assistant extracts the amount and recipient.
4. **Cancellation:** Review the transfer details and reply "No" to verify that the transfer is cancelled.
5. **Hinglish amount:** Enter "Rahul ko dedh hazaar rupaye bhejo." Verify that the amount is parsed as INR 1,500 and the recipient as Rahul.
6. **Second Hinglish example:** Enter "Mujhe Priya ko paanch sau rupaye bhejne hain." Verify that the amount is parsed as INR 500 and the recipient as Priya.
7. **Successful simulated transfer:** Request a transfer, review the details, reply "Yes", and enter the demo verification code `2468`.
8. **Voice interaction:** Enable assistant voice, use the microphone to speak a transfer request, and verify the assistant's spoken response.
9. **Automated tests:** Run `.\venv\Scripts\python.exe -m pytest -v` from the backend folder. The current test suite passed 13 tests.

## Safety Notes and Limitations

- This is a simulated banking demo. It does not connect to real bank accounts or move real money.
- The demo verification code is `2468`. Never use a real banking PIN or password.
- The voice challenge checks the spoken phrase but does not provide reliable speaker identity verification or liveness detection.
- Voice spoofing and replay-attack detection are not fully implemented.
- Transaction data is maintained by the demo backend and may reset when the server restarts.

