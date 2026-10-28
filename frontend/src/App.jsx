
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

  async function sendMessage(e) {
    if (e) e.preventDefault();

    const text = message.trim();

    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.reply || "Sorry, I couldn't understand that.",
        },
      ]);
    } catch (error) {
      console.error("Chat API error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Unable to connect to the banking service. Please check that the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function startVoiceInput() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Voice recognition is not supported in this browser. Please try an updated version of Google Chrome."
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
      console.log("Voice recognition started. Please speak.");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log("Recognized speech:", transcript);
      setMessage(transcript);
    };

    recognition.onerror = (event) => {
      console.error("Voice input error:", event.error);

      const errors = {
        "not-allowed":
          "Microphone access was denied. Check your browser permissions.",
        "service-not-allowed":
          "The browser's speech recognition service is blocked.",
        network:
          "Speech recognition could not connect to its service. Check your internet connection and try again.",
        "no-speech":
          "No speech was detected. Please speak closer to your microphone.",
        "audio-capture":
          "No microphone was detected. Check your microphone connection.",
        aborted:
          "Voice recognition was interrupted. Please try again.",
      };

      alert(
        errors[event.error] ||
          `Voice input failed: ${event.error}. Please try again.`
      );
    };

    recognition.onend = () => {
      setListening(false);
      console.log("Voice recognition ended.");
    };

    try {
      recognition.start();
    } catch (error) {
      setListening(false);
      console.error("Could not start voice recognition:", error);
      alert("Could not start voice input. Please try again.");
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
                {item.role === "user" ? "You" : "Banking Assistant"}
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
            aria-label="Use voice input"
            title="Speak your message"
            disabled={loading || listening}
          >
            {listening ? "🔴" : "🎙️"}
          </button>

          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={
              listening ? "Listening... speak now" : "Ask about banking..."
            }
            aria-label="Your message"
            disabled={loading}
          />

          <button
            className="send-button"
            type="submit"
            disabled={loading || !message.trim()}
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </form>

        <p className="disclaimer">
          Demo only. Never enter your PIN, password, or real
          banking details.
        </p>
      </section>
    </main>
  );
}

export default App;
