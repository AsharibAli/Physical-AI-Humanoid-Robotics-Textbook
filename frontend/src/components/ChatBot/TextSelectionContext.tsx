/**
 * Text Selection Context Component
 *
 * Captures text selection from documentation pages using window.getSelection() API.
 * Preserves Markdown context including code blocks and headers.
 *
 * Tasks: T089, T090, T091
 */

import React, { useEffect, useState, useCallback } from 'react';

export interface SelectionInfo {
  text: string;
  range: Range | null;
  isValid: boolean;
  wordCount: number;
  context?: {
    beforeText: string;
    afterText: string;
    containsCode: boolean;
    containsHeader: boolean;
  };
}

interface TextSelectionContextProps {
  onSelectionChange: (selection: SelectionInfo) => void;
  minWords?: number;
  maxWords?: number;
  children: React.ReactNode;
}

/**
 * Component that monitors text selection and provides context
 */
export const TextSelectionContext: React.FC<TextSelectionContextProps> = ({
  onSelectionChange,
  minWords = 20,
  maxWords = 2000,
  children,
}) => {
  const [selection, setSelection] = useState<SelectionInfo>({
    text: '',
    range: null,
    isValid: false,
    wordCount: 0,
  });

  const [showButton, setShowButton] = useState(false);
  const [buttonPosition, setButtonPosition] = useState({ top: 0, left: 0 });

  /**
   * Extract Markdown context from selection
   * Checks for code blocks, headers, and surrounding text
   */
  const extractMarkdownContext = useCallback((range: Range): SelectionInfo['context'] => {
    const container = range.commonAncestorContainer;
    const parentElement = container.nodeType === Node.TEXT_NODE
      ? container.parentElement
      : container as Element;

    if (!parentElement) {
      return {
        beforeText: '',
        afterText: '',
        containsCode: false,
        containsHeader: false,
      };
    }

    // Check if selection is within code block
    const isInCodeBlock = !!parentElement.closest('pre, code');

    // Check if selection is within header
    const isInHeader = !!parentElement.closest('h1, h2, h3, h4, h5, h6');

    // Get surrounding text for context
    const fullText = parentElement.textContent || '';
    const selectedText = range.toString();
    const selectedIndex = fullText.indexOf(selectedText);

    const beforeText = selectedIndex > 0
      ? fullText.substring(Math.max(0, selectedIndex - 50), selectedIndex)
      : '';

    const afterText = selectedIndex >= 0
      ? fullText.substring(
          selectedIndex + selectedText.length,
          Math.min(fullText.length, selectedIndex + selectedText.length + 50)
        )
      : '';

    return {
      beforeText,
      afterText,
      containsCode: isInCodeBlock,
      containsHeader: isInHeader,
    };
  }, []);

  /**
   * Handle text selection changes
   */
  const handleSelectionChange = useCallback(() => {
    const windowSelection = window.getSelection();

    if (!windowSelection || windowSelection.rangeCount === 0) {
      setSelection({
        text: '',
        range: null,
        isValid: false,
        wordCount: 0,
      });
      setShowButton(false);
      return;
    }

    const selectedText = windowSelection.toString().trim();

    if (!selectedText) {
      setSelection({
        text: '',
        range: null,
        isValid: false,
        wordCount: 0,
      });
      setShowButton(false);
      return;
    }

    const range = windowSelection.getRangeAt(0);
    const wordCount = selectedText.split(/\s+/).length;
    const isValid = wordCount >= minWords && wordCount <= maxWords;

    // Extract Markdown context (T090)
    const context = extractMarkdownContext(range);

    const selectionInfo: SelectionInfo = {
      text: selectedText,
      range,
      isValid,
      wordCount,
      context,
    };

    setSelection(selectionInfo);
    onSelectionChange(selectionInfo);

    // Show "Ask about selection" button if valid (T091)
    if (isValid) {
      const rect = range.getBoundingClientRect();
      setButtonPosition({
        top: rect.bottom + window.scrollY + 5,
        left: rect.left + window.scrollX,
      });
      setShowButton(true);
    } else {
      setShowButton(false);
    }
  }, [minWords, maxWords, extractMarkdownContext, onSelectionChange]);

  useEffect(() => {
    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('keyup', handleSelectionChange);
    document.addEventListener('touchend', handleSelectionChange);

    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('keyup', handleSelectionChange);
      document.removeEventListener('touchend', handleSelectionChange);
    };
  }, [handleSelectionChange]);

  return (
    <div className="text-selection-wrapper">
      {children}

      {/* T091: "Ask about selection" button */}
      {showButton && (
        <div
          className="selection-action-button"
          style={{
            position: 'absolute',
            top: `${buttonPosition.top}px`,
            left: `${buttonPosition.left}px`,
            zIndex: 1000,
          }}
        >
          <button
            className="ask-about-selection-btn"
            onClick={() => {
              // This will be handled by parent component
              // The parent should have access to the selection via onSelectionChange
            }}
            title={`Ask about this selection (${selection.wordCount} words)`}
          >
            Ask about selection
          </button>
          {!selection.isValid && (
            <span className="selection-hint">
              {selection.wordCount < minWords
                ? `Select at least ${minWords} words`
                : `Selection too long (max ${maxWords} words)`}
            </span>
          )}
        </div>
      )}
    </div>
  );
};

/**
 * Hook for using text selection context
 */
export const useTextSelection = (
  minWords: number = 20,
  maxWords: number = 2000
): SelectionInfo => {
  const [selection, setSelection] = useState<SelectionInfo>({
    text: '',
    range: null,
    isValid: false,
    wordCount: 0,
  });

  useEffect(() => {
    const handleSelection = () => {
      const windowSelection = window.getSelection();

      if (!windowSelection || windowSelection.rangeCount === 0) {
        setSelection({
          text: '',
          range: null,
          isValid: false,
          wordCount: 0,
        });
        return;
      }

      const selectedText = windowSelection.toString().trim();

      if (!selectedText) {
        setSelection({
          text: '',
          range: null,
          isValid: false,
          wordCount: 0,
        });
        return;
      }

      const wordCount = selectedText.split(/\s+/).length;
      const isValid = wordCount >= minWords && wordCount <= maxWords;

      setSelection({
        text: selectedText,
        range: windowSelection.getRangeAt(0),
        isValid,
        wordCount,
      });
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [minWords, maxWords]);

  return selection;
};

/**
 * Context Provider wrapper that works without requiring onSelectionChange prop
 * This is used in Root.tsx as a global provider
 */
export const TextSelectionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentSelection, setCurrentSelection] = useState<SelectionInfo>({
    text: '',
    range: null,
    isValid: false,
    wordCount: 0,
  });

  const handleSelectionChange = useCallback((selection: SelectionInfo) => {
    setCurrentSelection(selection);
  }, []);

  return (
    <TextSelectionContext onSelectionChange={handleSelectionChange}>
      {children}
    </TextSelectionContext>
  );
};

export default TextSelectionContext;
