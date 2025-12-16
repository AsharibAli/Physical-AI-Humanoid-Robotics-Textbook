/**
 * ChatBot Components Export
 *
 * Centralized exports for all chatbot-related components
 */

export { TextSelectionContext, useTextSelection, TextSelectionProvider } from './TextSelectionContext';
export type { SelectionInfo } from './TextSelectionContext';

export {
  QueryModeToggle,
  QueryModeToggleCompact,
  useQueryMode,
} from './QueryModeToggle';
export type { QueryMode } from './QueryModeToggle';

export { ChatKitWrapper } from './ChatKitWrapper';

// Re-export types for convenience
export type {
  SelectionInfo as TextSelection,
} from './TextSelectionContext';
