import React from 'react';
import { TextSelectionProvider } from '../components/ChatBot/TextSelectionContext';
import { ChatKitWrapper } from '../components/ChatBot/ChatKitWrapper';

// Docusaurus Root wrapper for global components
export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <TextSelectionProvider>
      {children}
      <ChatKitWrapper />
    </TextSelectionProvider>
  );
}
