/**
 * Integration Example for Text Selection with Chat
 *
 * This example demonstrates how to integrate TextSelectionContext
 * and QueryModeToggle components with a chat interface (T093).
 *
 * NOTE: This is an example/template. The actual chat integration
 * will happen in Phase 7 with @openai/chatkit-react.
 */

import React, { useState } from 'react';
import {
  TextSelectionContext,
  QueryModeToggle,
  useQueryMode,
  SelectionInfo,
  QueryMode,
} from './index';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  citations?: any[];
}

/**
 * Example integration component
 */
export const ChatWithSelection: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentQuery, setCurrentQuery] = useState('');
  const [selection, setSelection] = useState<SelectionInfo | null>(null);
  const { mode, setMode, isSelectedText } = useQueryMode('full-book');

  /**
   * Handle selection changes from TextSelectionContext
   */
  const handleSelectionChange = (selectionInfo: SelectionInfo) => {
    setSelection(selectionInfo);

    // Auto-switch to selected-text mode if valid selection
    if (selectionInfo.isValid) {
      setMode('selected-text');
    }
  };

  /**
   * Handle mode changes
   */
  const handleModeChange = (newMode: QueryMode) => {
    setMode(newMode);

    // If switching to full-book, clear selection
    if (newMode === 'full-book') {
      setSelection(null);
    }
  };

  /**
   * Submit query to backend API
   */
  const handleSubmitQuery = async () => {
    if (!currentQuery.trim()) return;

    const requestBody = {
      query_text: currentQuery,
      query_mode: mode,
      max_results: 5,
      ...(isSelectedText && selection?.isValid
        ? { selected_text: selection.text }
        : {}),
    };

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/api/v1/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      // Add user message
      setMessages((prev) => [
        ...prev,
        {
          role: 'user',
          content: currentQuery,
        },
      ]);

      // Add assistant response
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.response_text,
          citations: data.source_citations,
        },
      ]);

      // Clear query
      setCurrentQuery('');
    } catch (error) {
      console.error('Failed to submit query:', error);
      // Handle error appropriately
    }
  };

  return (
    <TextSelectionContext
      onSelectionChange={handleSelectionChange}
      minWords={20}
      maxWords={2000}
    >
      <div className="chat-container">
        {/* Query Mode Toggle */}
        <QueryModeToggle
          mode={mode}
          onModeChange={handleModeChange}
          hasSelection={selection?.isValid || false}
          selectionWordCount={selection?.wordCount}
        />

        {/* Selection Preview */}
        {isSelectedText && selection?.isValid && (
          <div className="selection-preview">
            <div className="preview-header">
              <span>Selected Text ({selection.wordCount} words)</span>
              <button onClick={() => setMode('full-book')}>✕</button>
            </div>
            <div className="preview-content">
              {selection.text.substring(0, 200)}
              {selection.text.length > 200 ? '...' : ''}
            </div>
          </div>
        )}

        {/* Chat Messages */}
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message message-${message.role}`}>
              <div className="message-content">{message.content}</div>
              {message.citations && message.citations.length > 0 && (
                <div className="message-citations">
                  <strong>Sources:</strong>
                  <ul>
                    {message.citations.map((citation, idx) => (
                      <li key={idx}>
                        {citation.chapter_title} - {citation.section_type}
                        <span className="relevance">
                          ({(citation.relevance_score * 100).toFixed(0)}% relevant)
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="chat-input-area">
          <input
            type="text"
            value={currentQuery}
            onChange={(e) => setCurrentQuery(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleSubmitQuery();
              }
            }}
            placeholder={
              isSelectedText
                ? 'Ask about your selected text...'
                : 'Ask a question about the textbook...'
            }
            className="chat-input"
          />
          <button
            onClick={handleSubmitQuery}
            disabled={!currentQuery.trim()}
            className="chat-submit-btn"
          >
            Send
          </button>
        </div>

        {/* Mode-specific hints */}
        {isSelectedText && !selection?.isValid && (
          <div className="input-hint warning">
            Please highlight at least 20 words from the documentation to use
            selected-text mode
          </div>
        )}
      </div>
    </TextSelectionContext>
  );
};

export default ChatWithSelection;
