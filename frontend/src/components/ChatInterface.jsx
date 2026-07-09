import React, { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { sendMessage, addUserMessage } from '../redux/chatSlice';
import { Send, Bot, User, Loader2 } from 'lucide-react';

const ChatInterface = () => {
  const [input, setInput] = useState('');
  const dispatch = useDispatch();
  const { messages, isLoading, sessionId, executionSteps } = useSelector((state) => state.chat);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, executionSteps]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    dispatch(addUserMessage(input));
    dispatch(sendMessage({ message: input, sessionId }));
    setInput('');
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <Bot className="text-primary-color" size={20} />
        <span>AI CRM Assistant</span>
      </div>
      
      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message-row ${msg.type}`}>
            <div className="chat-bubble-container">
              <div className={`avatar ${msg.type === 'user' ? 'user' : 'ai'}`}>
                {msg.type === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div className="chat-bubble">
                {msg.text}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="chat-message-row ai">
             <div className="chat-bubble-container">
              <div className="avatar ai">
                <Bot size={16} />
              </div>
              <div className="chat-bubble" style={{display: 'flex', flexDirection: 'column', gap: '8px'}}>
                <div style={{display: 'flex', alignItems: 'center', gap: '8px', fontWeight: '500'}}>
                  <Loader2 size={16} style={{animation: 'spin 1s linear infinite'}} color="var(--primary-color)"/>
                  <span>Agent is working...</span>
                </div>
                {executionSteps.length > 0 && (
                  <div style={{fontSize: '0.75rem', color: 'var(--text-muted)', borderTop: '1px solid var(--border-color)', paddingTop: '8px'}}>
                    {executionSteps.map((step, idx) => (
                      <div key={idx} style={{display: 'flex', alignItems: 'center', gap: '4px'}}>
                         <span style={{color: 'var(--success-text)'}}>✓</span> {step}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Log an interaction, e.g., 'Met with Dr. Sharma for 15 mins...'"
          className="chat-input"
          disabled={isLoading}
        />
        <button 
          type="submit" 
          disabled={!input.trim() || isLoading}
          className="send-btn"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
