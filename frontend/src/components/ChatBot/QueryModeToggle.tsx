/**
 * Query Mode Toggle Component
 *
 * Allows users to switch between full-book and selected-text query modes.
 *
 * Task: T092, T098
 */

import React from 'react';

export type QueryMode = 'full-book' | 'selected-text';

interface QueryModeToggleProps {
  mode: QueryMode;
  onModeChange: (mode: QueryMode) => void;
  hasSelection: boolean;
  selectionWordCount?: number;
  disabled?: boolean;
}

/**
 * Toggle component for switching between query modes
 */
export const QueryModeToggle: React.FC<QueryModeToggleProps> = ({
  mode,
  onModeChange,
  hasSelection,
  selectionWordCount = 0,
  disabled = false,
}) => {
  return (
    <div className="query-mode-toggle">
      <div className="toggle-container">
        <button
          className={`mode-button ${mode === 'full-book' ? 'active' : ''}`}
          onClick={() => onModeChange('full-book')}
          disabled={disabled}
          aria-label="Search entire book"
          title="Search across all chapters and sections"
        >
          <span className="mode-icon">📚</span>
          <span className="mode-label">Full Book</span>
        </button>

        <button
          className={`mode-button ${mode === 'selected-text' ? 'active' : ''}`}
          onClick={() => onModeChange('selected-text')}
          disabled={disabled || !hasSelection}
          aria-label="Ask about selected text"
          title={
            hasSelection
              ? `Ask about your selection (${selectionWordCount} words)`
              : 'Highlight text to enable this mode'
          }
        >
          <span className="mode-icon">✨</span>
          <span className="mode-label">
            Selected Text
            {hasSelection && <span className="word-count">({selectionWordCount})</span>}
          </span>
        </button>
      </div>

      <div className="mode-description">
        {mode === 'full-book' ? (
          <p>Searching across the entire textbook content</p>
        ) : (
          <p>Focusing on your highlighted text</p>
        )}
      </div>

      {mode === 'selected-text' && !hasSelection && (
        <div className="mode-hint warning">
          Please highlight text from the documentation to use this mode
        </div>
      )}
    </div>
  );
};

/**
 * Compact version for smaller UI areas
 */
export const QueryModeToggleCompact: React.FC<QueryModeToggleProps> = ({
  mode,
  onModeChange,
  hasSelection,
  disabled = false,
}) => {
  return (
    <div className="query-mode-toggle-compact">
      <label className="toggle-switch">
        <input
          type="checkbox"
          checked={mode === 'selected-text'}
          onChange={(e) => onModeChange(e.target.checked ? 'selected-text' : 'full-book')}
          disabled={disabled || !hasSelection}
        />
        <span className="toggle-slider"></span>
      </label>
      <span className="toggle-label">
        {mode === 'full-book' ? 'Full Book' : 'Selection'}
      </span>
    </div>
  );
};

/**
 * Hook for managing query mode state
 */
export const useQueryMode = (initialMode: QueryMode = 'full-book') => {
  const [mode, setMode] = React.useState<QueryMode>(initialMode);

  const switchToFullBook = React.useCallback(() => {
    setMode('full-book');
  }, []);

  const switchToSelectedText = React.useCallback(() => {
    setMode('selected-text');
  }, []);

  const toggleMode = React.useCallback(() => {
    setMode((prev) => (prev === 'full-book' ? 'selected-text' : 'full-book'));
  }, []);

  return {
    mode,
    setMode,
    switchToFullBook,
    switchToSelectedText,
    toggleMode,
    isFullBook: mode === 'full-book',
    isSelectedText: mode === 'selected-text',
  };
};

export default QueryModeToggle;
