
import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hello! Welcome to Voice Banking. How can I help you today?",
    },
  ]);

  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [challenge, setChallenge] = useState("");
  const [challengePassed, setChallengePassed] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);

  // Speak assistant messages.
  function speakReply(text) {
    if (!("speechSynthesis" in window) || !voiceEnabled) {
      return;
    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-IN";
    speech.rate = 0.95;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.speak(speech);
  }

  // Enable voice using a direct button click.
  function enableVoice() {
    if (!("speechSynthesis" in window)) {
      alert("Text-to-speech is not supported in this browser.");
      return;
    }

    setVoiceEnabled(true);

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(
      "Voice replies are now enabled."
    );

    speech.lang = "en-IN";
    speech.rate = 0.95;
    speech.volume = 1;

    window.speechSynthesis.speak(speech);
  }

  // Disable assistant voice.
  function disableVoice() {
    window.speechSynthesis.cancel();
    setVoiceEnabled(false);
  }

  // Send a message to FastAPI.
  async function sendMessage(e) {
    e.preventDefault();

    const text = message.trim();

    if (!text || loading || challenge) {
      return;
    }

    setMessages((prev) => [
      ...prev,
      { role: "user", text },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: text }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }

      const reply =
        data.reply || "Sorry, I couldn't understand that.";

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: reply },
      ]);

      speakReply(reply);
    } catch (error) {
      console.error("Chat API error:", error);

      const errorMessage =
        "Unable to connect to the banking service. Please check the backend.";

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: errorMessage },
      ]);

      speakReply(errorMessage);
    } finally {
      setLoading(false);
    }
  }

  // Start a random phrase challenge.
  function startLivenessChallenge() {
    const phrases = [
      "My voice is my choice",
      "I am speaking now",
      "Today is a good day",
    ];

    const selectedPhrase =
      phrases[Math.floor(Math.random() * phrases.length)];

    setChallenge(selectedPhrase);
    setChallengePassed(false);
    setMessage("");

    const reply =
      `Please speak this challenge phrase: ${selectedPhrase}`;

    setMessages((prev) => [
      ...prev,
      { role: "assistant", text: reply },
    ]);

    speakReply(reply);
  }

  // Start microphone recognition.
  function startVoiceInput() {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Voice recognition is not supported. Please use an updated version of Google Chrome."
      );
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      const transcript =
        event.results[0][0].transcript.trim();

      // Check challenge phrase if a challenge is active.
      if (challenge) {
        setMessages((prev) => [
          ...prev,
          { role: "user", text: transcript },
        ]);

        const spoken = transcript.toLowerCase();
        const expected = challenge.toLowerCase();

        if (spoken === expected) {
          setChallengePassed(true);
          setChallenge("");

          const reply =
            "Challenge phrase matched. This demo challenge is complete.";

          setMessages((prev) => [
            ...prev,
            { role: "assistant", text: reply },
          ]);

          speakReply(reply);
        } else {
          const reply =
            "The phrase did not match. Please try the challenge again.";

          setMessages((prev) => [
            ...prev,
            { role: "assistant", text: reply },
          ]);

          speakReply(reply);
        }

        return;
      }

      // Normal voice input goes into the message box.
      setMessage(transcript);
    };

    recognition.onerror = (event) => {
      console.error("Voice recognition error:", event.error);

      if (event.error !== "no-speech") {
        alert(
          "Voice input failed: " +
            event.error +
            ". Please try typing."
        );
      }
    };

    recognition.onend = () => {
      setListening(false);
    };

    try {
      recognition.start();
    } catch (error) {
      setListening(false);
      console.error("Could not start voice input:", error);
    }
  }

  return (
    <main className="app">
      <header className="header">
        <div className="brand-icon">₹</div>

        <div>
          <h1>Voice Banking</h1>
          <p>Your personal banking assistant</p>
        </div>

        <span className="status">● Assistant</span>
      </header>

      <section className="hero">
        <div className="hero-icon">🎙️</div>
        <h2>Banking made simpler.</h2>
        <p>Ask a question by typing or using your voice.</p>
      </section>

      <section className="chat">
        <div className="chat-heading">
          <h3>Conversation</h3>
          <span>English (India)</span>
        </div>

        <div className="messages" aria-live="polite">
          {messages.map((item, index) => (
            <div
              className={`message ${item.role}`}
              key={index}
            >
              <span className="message-label">
                {item.role === "user"
                  ? "You"
                  : "Banking Assistant"}
              </span>

              <p>{item.text}</p>
            </div>
          ))}

          {loading && (
            <p className="loading">Thinking...</p>
          )}
        </div>

        <form className="composer" onSubmit={sendMessage}>
          <button
            type="button"
            className="voice-button"
            onClick={startVoiceInput}
            disabled={loading || listening}
            aria-label="Use voice input"
            title="Speak your message"
          >
            {listening ? "🔴" : "🎙️"}
          </button>

          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={
              listening
                ? "Listening... speak now"
                : "Ask about banking..."
            }
            aria-label="Your message"
            disabled={loading || Boolean(challenge)}
          />

          <button
            className="send-button"
            type="submit"
            disabled={
              loading || !message.trim() || Boolean(challenge)
            }
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </form>

        <div className="challenge-section">
          <button
            type="button"
            className="send-button"
            onClick={startLivenessChallenge}
            disabled={listening || loading}
          >
            Start Voice Challenge
          </button>

          {challengePassed && (
            <p>Voice challenge completed for this demo.</p>
          )}

          <p className="disclaimer">
            Demo challenge only. This does not prove that a
            voice is live or detect replayed or synthetic audio.
          </p>
        </div>

        <div className="challenge-section">
          {voiceEnabled ? (
            <button
              type="button"
              className="send-button"
              onClick={disableVoice}
            >
              Turn Voice Replies Off
            </button>
          ) : (
            <button
              type="button"
              className="send-button"
              onClick={enableVoice}
            >
              Enable Assistant Voice
            </button>
          )}
        </div>

        <p className="disclaimer">
          Demo only. Never enter your real PIN, password,
          or banking details.
        </p>
      </section>
    </main>
  );
}

export default App;
