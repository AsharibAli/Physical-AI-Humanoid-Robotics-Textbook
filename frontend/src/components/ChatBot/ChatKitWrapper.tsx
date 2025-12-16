import React, { useState, useEffect } from 'react';
import { SimpleChatInterface } from './SimpleChatInterface';

export const ChatKitWrapper: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Detect theme changes
  useEffect(() => {
    const updateTheme = () => {
      const theme = document.documentElement.getAttribute('data-theme');
      setIsDarkMode(theme === 'dark');
    };

    updateTheme();

    // Watch for theme changes
    const observer = new MutationObserver(updateTheme);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    });

    return () => observer.disconnect();
  }, []);

  // Theme-aware colors
  const bgColor = isDarkMode ? '#ffffff' : '#000000';
  const textColor = isDarkMode ? '#000000' : '#ffffff';
  const hoverBgColor = isDarkMode ? '#000000' : '#ffffff';
  const hoverTextColor = isDarkMode ? '#ffffff' : '#000000';

  if (isCollapsed) {
    return (
      <button
        onClick={() => setIsCollapsed(false)}
        className="chatbot-toggle-button"
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          width: '60px',
          height: '60px',
          borderRadius: '0',
          backgroundColor: bgColor,
          color: textColor,
          border: `2px solid ${bgColor}`,
          boxShadow: isDarkMode
            ? '0 4px 12px rgba(255, 255, 255, 0.3)'
            : '0 4px 12px rgba(0, 0, 0, 0.3)',
          cursor: 'pointer',
          fontSize: '24px',
          zIndex: 1000,
          transition: 'all 0.3s ease'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = hoverBgColor;
          e.currentTarget.style.color = hoverTextColor;
          e.currentTarget.style.transform = 'scale(1.05)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = bgColor;
          e.currentTarget.style.color = textColor;
          e.currentTarget.style.transform = 'scale(1)';
        }}
        title="Open AI Assistant"
      >
        💬
      </button>
    );
  }

  return (
    <div
      className="chatkit-container"
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: 1000,
        boxShadow: isDarkMode
          ? '0 4px 24px rgba(255, 255, 255, 0.3)'
          : '0 4px 24px rgba(0, 0, 0, 0.3)',
        borderRadius: '0',
        overflow: 'hidden',
        backgroundColor: isDarkMode ? '#000000' : '#ffffff',
        border: `2px solid ${bgColor}`
      }}
    >
      <div style={{
        padding: '12px 16px',
        background: bgColor,
        color: textColor,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: `2px solid ${bgColor}`
      }}>
        <span style={{ fontWeight: 600 }}>AI Assistant</span>
        <button
          onClick={() => setIsCollapsed(true)}
          style={{
            background: 'none',
            border: 'none',
            color: textColor,
            fontSize: '20px',
            cursor: 'pointer',
            padding: '0 8px',
            transition: 'opacity 0.2s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.opacity = '0.7';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.opacity = '1';
          }}
          title="Minimize"
        >
          ✕
        </button>
      </div>
      <SimpleChatInterface isDarkMode={isDarkMode} />
    </div>
  );
};
