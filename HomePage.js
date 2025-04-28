import React, { useState, useEffect, useRef } from 'react';
import './HomePage.css';

const HomePage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const chatWindowRef = useRef(null);

  // Generate a unique session ID on component mount
  useEffect(() => {
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substring(2)}`;
    setSessionId(newSessionId);
    // Add a welcome message
    setMessages([
      {
        sender: 'bot',
        text: "Hello! I'm ASHA AI Bot. I can help with jobs, events, mentorships, or FAQs. What are you looking for?",
      },
    ]);
  }, []);

  // Scroll to the bottom of the chat window when new messages are added
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  // Function to send a message to the backend
  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    // Add user's message to the chat
    const userMessage = { sender: 'user', text: messageText };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    try {
      const response = await fetch('http://127.0.0.1:8000/chatbot/query/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      const botMessage = { sender: 'bot', text: data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        sender: 'bot',
        text: "Sorry, something went wrong. Please try again or contact support at support@asha.ai.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  // Handle input submission
  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
  };

  // Handle FAQ button clicks
  const handleFaqClick = (faqQuestion) => {
    sendMessage(faqQuestion);
  };

  // Handle feedback submission
  const handleFeedback = (messageIndex) => {
    const feedback = prompt("Please provide feedback for this response:");
    if (feedback) {
      console.log(`Feedback for message ${messageIndex}: ${feedback}`);
      alert("Thank you for your feedback! We’ll use it to improve.");
      // In a real app, send feedback to the backend (e.g., via a new API endpoint)
    }
  };

  return (
    <div className="asha-ai-bot">
      {/* Header */}
      <header className="header">
        <h1>ASHA AI BOT</h1>
        <nav>
          <a href="/signup">Sign Up</a>
          <a href="#">Share</a>
          <a href="/contact">Contact</a>
          <div className="user-icon">👤</div>
        </nav>
      </header>

      <div className="main-container">
        {/* Sidebar */}
        <aside className="sidebar">
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="#">Recents</a></li>
            <li><a href="#">Job Opportunities</a></li>
            <li><a href="#">Community</a></li>
            <li><a href="#">Membership</a></li>
            <li><a href="#">Privacy</a></li>
          </ul>
        </aside>

        {/* Chat Section */}
        <section className="chat-section">
          <h2>CHAT BOT</h2>
          <div className="chat-window" ref={chatWindowRef}>
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}>
                {msg.text}
                {msg.sender === 'bot' && (
                  <button
                    className="feedback-button"
                    onClick={() => handleFeedback(index)}
                  >
                    Feedback
                  </button>
                )}
              </div>
            ))}
          </div>
          <form onSubmit={handleSubmit} className="chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask ASHA..."
            />
            <button type="submit" className="send-button">
              <span role="img" aria-label="Send">🚀</span>
            </button>
          </form>
        </section>

        {/* FAQ Section */}
        <aside className="faq-section">
          <h2>FAQ</h2>
          <button onClick={() => handleFaqClick('How do I apply for jobs?')}>
            How do I apply for jobs?
          </button>
          <button onClick={() => handleFaqClick('What is Membership?')}>
            What is Membership?
          </button>
          <button onClick={() => handleFaqClick('How can I reset my password?')}>
            How can I reset my password?
          </button>
          <button onClick={() => handleFaqClick('How do I contact support?')}>
            How do I contact support?
          </button>
        </aside>
      </div>
    </div>
  );
};

export default HomePage;