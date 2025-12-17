import React, { useState, useRef, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface SimpleChatInterfaceProps {
  isDarkMode: boolean;
  onClearHistory?: () => void;
}

export const SimpleChatInterface: React.FC<SimpleChatInterfaceProps> = ({ isDarkMode, onClearHistory }) => {
  const { siteConfig } = useDocusaurusContext();

  // Determine backend URL based on environment
  const getBackendUrl = () => {
    // If running on localhost, use local backend
    if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
      return 'http://localhost:8000';
    }
    // Otherwise use configured backend URL
    return siteConfig.customFields?.backendApiUrl as string || 'http://localhost:8000';
  };

  const backendApiUrl = getBackendUrl();

  // Load messages from localStorage on mount
  const [messages, setMessages] = useState<Message[]>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('chatMessages');
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          // Convert timestamp strings back to Date objects
          return parsed.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          }));
        } catch (e) {
          console.error('Error loading messages:', e);
        }
      }
    }
    return [
      {
        role: 'assistant',
        content: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. Ask me anything!',
        timestamp: new Date()
      }
    ];
  });

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const bgColor = isDarkMode ? '#000000' : '#ffffff';
  const textColor = isDarkMode ? '#ffffff' : '#000000';
  const borderColor = isDarkMode ? '#404040' : '#d4d4d4';
  const userMsgBg = isDarkMode ? '#1a1a1a' : '#f5f5f5';
  const assistantMsgBg = isDarkMode ? '#0a0a0a' : '#ffffff';

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('chatMessages', JSON.stringify(messages));
    }
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call backend query endpoint
      const response = await fetch(`${backendApiUrl}/api/v1/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query_text: input,
          query_mode: 'full-book',
          max_results: 5
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response_text || 'Sorry, I couldn\'t generate a response.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure:\n1. The backend server is running on port 8000\n2. Content has been ingested into Qdrant\n3. Your OpenAI API key is configured',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '600px',
        width: '400px',
        backgroundColor: bgColor,
        color: textColor
      }}
    >
      {/* Messages area */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '80%'
            }}
          >
            <div
              style={{
                padding: '8px 12px',
                backgroundColor: msg.role === 'user' ? userMsgBg : assistantMsgBg,
                border: `1px solid ${borderColor}`,
                borderRadius: '0',
                fontSize: '14px',
                lineHeight: '1.5',
                whiteSpace: 'pre-wrap',
                wordWrap: 'break-word'
              }}
            >
              <div style={{ fontWeight: 600, marginBottom: '4px', fontSize: '12px', opacity: 0.7 }}>
                {msg.role === 'user' ? 'You' : 'AI Assistant'}
              </div>
              {msg.content}
            </div>
            <div style={{ fontSize: '11px', opacity: 0.5, marginTop: '4px', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
              {msg.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}

        {isLoading && (
          <div
            style={{
              alignSelf: 'flex-start',
              padding: '8px 12px',
              backgroundColor: assistantMsgBg,
              border: `1px solid ${borderColor}`,
              fontSize: '14px',
              fontStyle: 'italic',
              opacity: 0.7
            }}
          >
            Thinking...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div
        style={{
          borderTop: `2px solid ${borderColor}`,
          padding: '16px',
          display: 'flex',
          gap: '8px'
        }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about the textbook..."
          disabled={isLoading}
          style={{
            flex: 1,
            padding: '8px 12px',
            backgroundColor: bgColor,
            color: textColor,
            border: `1px solid ${borderColor}`,
            borderRadius: '0',
            fontSize: '14px',
            outline: 'none'
          }}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
          style={{
            padding: '8px 16px',
            backgroundColor: textColor,
            color: bgColor,
            border: `1px solid ${textColor}`,
            borderRadius: '0',
            fontSize: '14px',
            fontWeight: 600,
            cursor: isLoading || !input.trim() ? 'not-allowed' : 'pointer',
            opacity: isLoading || !input.trim() ? 0.5 : 1
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};
