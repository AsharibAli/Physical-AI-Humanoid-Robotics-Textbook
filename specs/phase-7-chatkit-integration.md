# Phase 7: ChatKit Integration Specification

**Feature**: OpenAI ChatKit Integration for AI-Powered Q&A Interface
**Priority**: P1 (High)
**Estimated Tasks**: 18 tasks (T096-T113)
**Dependencies**: Phase 5 (RAG Backend), Phase 6 (Text Selection Context)

## Overview

Phase 7 integrates OpenAI's ChatKit framework to provide a production-ready, batteries-included chat experience for the Physical AI & Humanoid Robotics textbook. ChatKit replaces the originally planned custom chat UI with a professional, feature-rich solution that includes streaming responses, tool/workflow visualization, rich widgets, and deep customization capabilities.

### What is ChatKit?

ChatKit is OpenAI's official framework-agnostic chat component that delivers:
- **Deep UI customization** that feels native to your application
- **Built-in response streaming** for natural, interactive conversations
- **Tool and workflow integration** for visualizing agentic actions and chain-of-thought reasoning
- **Rich interactive widgets** rendered directly inside the chat
- **Attachment handling** with file and image upload support
- **Thread and message management** for complex conversations
- **Source annotations and entity tagging** for transparency

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Docusaurus)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  ChatKit Component (@openai/chatkit-react)            │ │
│  │  - useChatKit() hook                                   │ │
│  │  - Session management via client_secret               │ │
│  │  - Streaming message display                          │ │
│  │  - Custom UI theming                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  TextSelectionContext (Phase 6)                       │ │
│  │  - Selection monitoring                                │ │
│  │  - QueryModeToggle                                     │ │
│  │  - Context preservation                                │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  ChatKit Session Endpoints                            │ │
│  │  - POST /api/chatkit/session (create session)         │ │
│  │  - POST /api/chatkit/refresh (refresh session)        │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  RAG Service (Phase 5)                                │ │
│  │  - process_query()                                     │ │
│  │  - retrieve_for_selected_text()                        │ │
│  │  - generate_response()                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  OpenAI Client                                         │ │
│  │  - chatkit.sessions.create()                           │ │
│  │  - chatkit.sessions.refresh()                          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ OpenAI API
                             ▼
┌─────────────────────────────────────────────────────────────┐
│               OpenAI ChatKit Backend Service                 │
│  - Session management                                        │
│  - Message streaming                                         │
│  - Tool execution orchestration                              │
│  - Context management                                        │
└─────────────────────────────────────────────────────────────┘
```

## Integration Strategy

### Option 1: ChatKit Direct Integration (Recommended)

**Description**: Use ChatKit's built-in capabilities to handle RAG queries through OpenAI's infrastructure.

**Flow**:
1. Frontend creates ChatKit session with our backend token endpoint
2. User sends message through ChatKit UI
3. ChatKit routes message to OpenAI backend
4. Our backend provides custom tools/functions for RAG retrieval
5. OpenAI orchestrates tool calls and response generation
6. ChatKit displays streaming response with citations

**Pros**:
- Native streaming support
- Built-in tool/workflow visualization
- Minimal custom code
- Professional UI out-of-the-box
- Source annotations built-in

**Cons**:
- Requires OpenAI API key and ChatKit access
- Additional API costs for ChatKit service
- Less control over exact retrieval logic

### Option 2: Hybrid Approach (If ChatKit Direct Not Available)

**Description**: Use ChatKit UI but route queries through our existing RAG backend.

**Flow**:
1. ChatKit UI for message display and interaction
2. Custom message handler intercepts queries
3. Route to our FastAPI RAG service
4. Stream responses back to ChatKit
5. Format citations as ChatKit annotations

**Pros**:
- Full control over RAG pipeline
- Use existing Phase 5 infrastructure
- No changes to backend logic

**Cons**:
- More custom integration code
- May lose some ChatKit native features
- Need to adapt streaming format

## Implementation Tasks

### Backend Tasks (T096-T103)

#### T096: Install OpenAI Python SDK with ChatKit Support
**Objective**: Update backend dependencies to include ChatKit-enabled OpenAI SDK.

**File**: `backend/requirements.txt`

```txt
openai>=1.54.0  # ChatKit support requires v1.54+
```

**Acceptance Criteria**:
- [ ] OpenAI SDK v1.54+ installed
- [ ] `openai.chatkit` module accessible
- [ ] Backward compatibility with existing RAG code maintained

---

#### T097: Create ChatKit Configuration
**Objective**: Configure ChatKit session parameters and tools.

**New File**: `backend/config/chatkit_config.py`

```python
from pydantic_settings import BaseSettings
from typing import List, Dict, Any

class ChatKitConfig(BaseSettings):
    """ChatKit session configuration"""

    # Model configuration
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000

    # Session settings
    session_ttl: int = 3600  # 1 hour
    max_messages_per_session: int = 50

    # Tool definitions (for RAG integration)
    tools: List[Dict[str, Any]] = [
        {
            "type": "function",
            "function": {
                "name": "search_textbook",
                "description": "Search the Physical AI & Humanoid Robotics textbook for relevant information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to find relevant textbook content"
                        },
                        "selected_text": {
                            "type": "string",
                            "description": "Optional highlighted text from the textbook for context-aware search"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of relevant chunks to retrieve",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]

    # Custom instructions
    system_instructions: str = """You are an expert AI assistant for the Physical AI & Humanoid Robotics textbook.

Your role is to help students understand robotics concepts, ROS 2 programming, simulation,
perception, locomotion, manipulation, and control systems.

Guidelines:
1. Provide clear, accurate explanations based on the textbook content
2. Use the search_textbook tool to find relevant information
3. Cite specific chapters and sections when referencing material
4. When users highlight text, prioritize explaining that specific content
5. Offer code examples and practical insights when appropriate
6. Maintain a helpful, educational tone

Always ground your responses in the textbook content retrieved via search_textbook."""

    class Config:
        env_prefix = "CHATKIT_"

chatkit_config = ChatKitConfig()
```

**Acceptance Criteria**:
- [ ] Configuration file created with session parameters
- [ ] `search_textbook` tool defined with proper schema
- [ ] System instructions tailored to textbook domain
- [ ] Environment variable overrides supported

---

#### T098: Implement ChatKit Session Management
**Objective**: Create endpoints for ChatKit session creation and refresh.

**New File**: `backend/api/routes/chatkit.py`

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from openai import OpenAI
from typing import Optional
import logging

from backend.config.settings import settings
from backend.config.chatkit_config import chatkit_config

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chatkit", tags=["chatkit"])

# OpenAI client
openai_client = OpenAI(api_key=settings.openai_api_key)

class SessionResponse(BaseModel):
    """ChatKit session response"""
    client_secret: str
    session_id: str
    expires_at: int

class SessionRefreshRequest(BaseModel):
    """Session refresh request"""
    existing_session_id: str

@router.post("/session", response_model=SessionResponse)
async def create_chatkit_session():
    """
    Create a new ChatKit session.

    Returns client_secret for frontend ChatKit initialization.
    """
    try:
        session = openai_client.chatkit.sessions.create(
            model=chatkit_config.model,
            temperature=chatkit_config.temperature,
            max_tokens=chatkit_config.max_tokens,
            tools=chatkit_config.tools,
            instructions=chatkit_config.system_instructions,
            ttl=chatkit_config.session_ttl
        )

        return SessionResponse(
            client_secret=session.client_secret,
            session_id=session.id,
            expires_at=session.expires_at
        )

    except Exception as e:
        logger.error(f"Failed to create ChatKit session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create chat session: {str(e)}"
        )

@router.post("/refresh", response_model=SessionResponse)
async def refresh_chatkit_session(request: SessionRefreshRequest):
    """
    Refresh an existing ChatKit session.

    Extends session TTL without losing conversation history.
    """
    try:
        session = openai_client.chatkit.sessions.refresh(
            session_id=request.existing_session_id,
            ttl=chatkit_config.session_ttl
        )

        return SessionResponse(
            client_secret=session.client_secret,
            session_id=session.id,
            expires_at=session.expires_at
        )

    except Exception as e:
        logger.error(f"Failed to refresh ChatKit session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refresh chat session: {str(e)}"
        )
```

**Update**: `backend/api/main.py`

```python
from backend.api.routes import chatkit

# Include ChatKit router
app.include_router(chatkit.router)
```

**Acceptance Criteria**:
- [ ] `/api/chatkit/session` endpoint creates new sessions
- [ ] `/api/chatkit/refresh` endpoint extends existing sessions
- [ ] Proper error handling for OpenAI API failures
- [ ] Session metadata returned to frontend
- [ ] Endpoints registered in main FastAPI app

---

#### T099: Implement RAG Tool Handler
**Objective**: Create handler for `search_textbook` tool calls from ChatKit.

**New File**: `backend/services/chatkit_tools.py`

```python
from typing import Dict, Any, Optional
import logging

from backend.services.rag_service import RAGService

logger = logging.getLogger(__name__)

class ChatKitToolHandler:
    """Handles tool calls from ChatKit sessions"""

    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service

    async def handle_search_textbook(
        self,
        query: str,
        selected_text: Optional[str] = None,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Handle search_textbook tool call.

        Args:
            query: User's search query
            selected_text: Optional highlighted text for context-aware search
            max_results: Maximum chunks to retrieve

        Returns:
            Formatted tool response with textbook content and citations
        """
        try:
            # Determine query mode based on selected_text
            query_mode = "selected-text" if selected_text else "full-book"

            # Call RAG service (reuse Phase 5 infrastructure)
            result = await self.rag_service.process_query(
                query_text=query,
                query_mode=query_mode,
                selected_text=selected_text,
                max_results=max_results
            )

            # Format for ChatKit tool response
            formatted_result = {
                "status": "success",
                "content": result.response_text,
                "citations": [
                    {
                        "source": f"{cite.module_id}/{cite.chapter_id}",
                        "title": cite.chapter_title,
                        "section": cite.section_type,
                        "relevance": cite.relevance_score,
                        "text_preview": cite.chunk_text[:200] + "..."
                    }
                    for cite in result.source_citations
                ],
                "confidence": result.confidence_score,
                "chunks_retrieved": result.retrieved_chunks
            }

            return formatted_result

        except Exception as e:
            logger.error(f"Error in search_textbook tool: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to search textbook. Please try again."
            }

    async def route_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route tool calls to appropriate handlers.

        Args:
            tool_name: Name of the tool being called
            arguments: Tool arguments from ChatKit

        Returns:
            Tool execution result
        """
        if tool_name == "search_textbook":
            return await self.handle_search_textbook(**arguments)
        else:
            return {
                "status": "error",
                "error": f"Unknown tool: {tool_name}"
            }
```

**Acceptance Criteria**:
- [ ] `handle_search_textbook()` integrates with Phase 5 RAG service
- [ ] Tool responses formatted for ChatKit consumption
- [ ] Citations included in structured format
- [ ] Error handling for RAG failures
- [ ] Support for both full-book and selected-text modes

---

#### T100: Register Tool Endpoints (If Required)

**Note**: Depending on ChatKit's architecture, tool execution may be:
- **Option A**: Handled automatically by OpenAI's backend (tools execute server-side)
- **Option B**: Require webhook endpoints on our backend

**If Option B**, create:

**New File**: `backend/api/routes/chatkit_tools.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from backend.services.chatkit_tools import ChatKitToolHandler
from backend.services.rag_service import RAGService
from backend.services.retrieval_service import RetrievalService
from backend.services.response_generator import ResponseGenerator

router = APIRouter(prefix="/api/chatkit/tools", tags=["chatkit-tools"])

# Initialize tool handler
rag_service = RAGService(
    retrieval_service=RetrievalService(),
    response_generator=ResponseGenerator()
)
tool_handler = ChatKitToolHandler(rag_service)

class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    session_id: str

class ToolCallResponse(BaseModel):
    result: Dict[str, Any]

@router.post("/execute", response_model=ToolCallResponse)
async def execute_tool(request: ToolCallRequest):
    """Execute a tool call from ChatKit"""
    result = await tool_handler.route_tool_call(
        tool_name=request.tool_name,
        arguments=request.arguments
    )

    return ToolCallResponse(result=result)
```

**Acceptance Criteria**:
- [ ] Tool execution endpoint created (if needed)
- [ ] Webhook URL configurable in ChatKit session
- [ ] Tool results returned in expected format
- [ ] Authentication/authorization for tool calls (if required)

---

#### T101: Add Environment Variables
**Objective**: Update environment configuration for ChatKit.

**Update**: `backend/.env.example`

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...

# ChatKit Configuration (optional overrides)
CHATKIT_MODEL=gpt-4
CHATKIT_TEMPERATURE=0.7
CHATKIT_MAX_TOKENS=2000
CHATKIT_SESSION_TTL=3600
```

**Update**: `backend/config/settings.py`

```python
class Settings(BaseSettings):
    # ... existing settings ...

    # ChatKit settings (with defaults)
    chatkit_model: str = "gpt-4"
    chatkit_temperature: float = 0.7
```

**Acceptance Criteria**:
- [ ] `.env.example` includes ChatKit variables
- [ ] Settings model updated with ChatKit configuration
- [ ] Defaults provided for all ChatKit settings

---

#### T102: Update API Documentation
**Objective**: Document ChatKit endpoints in OpenAPI schema.

**Update**: Add docstrings and examples to all ChatKit endpoints

**Acceptance Criteria**:
- [ ] All endpoints have comprehensive docstrings
- [ ] Example request/response bodies provided
- [ ] OpenAPI schema generated correctly
- [ ] Available at `/docs` endpoint

---

#### T103: Backend Integration Testing
**Objective**: Test ChatKit session creation and tool execution.

**New File**: `backend/tests/test_chatkit_integration.py`

```python
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_create_chatkit_session():
    """Test ChatKit session creation"""
    response = client.post("/api/chatkit/session")
    assert response.status_code == 200
    data = response.json()
    assert "client_secret" in data
    assert "session_id" in data
    assert "expires_at" in data

def test_refresh_chatkit_session():
    """Test ChatKit session refresh"""
    # First create a session
    create_response = client.post("/api/chatkit/session")
    session_id = create_response.json()["session_id"]

    # Then refresh it
    response = client.post(
        "/api/chatkit/refresh",
        json={"existing_session_id": session_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id

@pytest.mark.asyncio
async def test_search_textbook_tool():
    """Test search_textbook tool handler"""
    from backend.services.chatkit_tools import ChatKitToolHandler
    from unittest.mock import AsyncMock

    # Mock RAG service
    mock_rag = AsyncMock()
    handler = ChatKitToolHandler(mock_rag)

    result = await handler.handle_search_textbook(
        query="What is ROS 2?",
        max_results=5
    )

    assert result["status"] == "success"
    assert "content" in result
    assert "citations" in result
```

**Acceptance Criteria**:
- [ ] Session creation tests pass
- [ ] Session refresh tests pass
- [ ] Tool handler tests pass
- [ ] Error cases covered

---

### Frontend Tasks (T104-T111)

#### T104: Install ChatKit React Package
**Objective**: Add ChatKit React bindings to frontend.

**File**: `frontend/package.json`

```bash
cd frontend
pnpm add @openai/chatkit-react
```

**Acceptance Criteria**:
- [ ] `@openai/chatkit-react` installed
- [ ] Version compatible with backend OpenAI SDK
- [ ] No dependency conflicts

---

#### T105: Add ChatKit Script to HTML
**Objective**: Include ChatKit JavaScript in the document head.

**Update**: `frontend/docusaurus.config.ts`

```typescript
const config: Config = {
  // ... existing config ...

  scripts: [
    {
      src: 'https://cdn.platform.openai.com/deployments/chatkit/chatkit.js',
      async: true,
    },
  ],

  // ... rest of config ...
};
```

**Acceptance Criteria**:
- [ ] ChatKit script included in all pages
- [ ] Script loads asynchronously
- [ ] No CORS or CSP issues

---

#### T106: Create ChatKit Integration Component
**Objective**: Build main ChatKit component with session management.

**New File**: `frontend/src/components/ChatBot/ChatKitWrapper.tsx`

```typescript
import React, { useCallback } from 'react';
import { ChatKit, useChatKit } from '@openai/chatkit-react';

interface ChatKitWrapperProps {
  className?: string;
  onError?: (error: Error) => void;
}

export const ChatKitWrapper: React.FC<ChatKitWrapperProps> = ({
  className = "h-[600px] w-[400px]",
  onError
}) => {
  const getClientSecret = useCallback(async (existingSessionId?: string) => {
    try {
      if (existingSessionId) {
        // Refresh existing session
        const res = await fetch('/api/chatkit/refresh', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ existing_session_id: existingSessionId })
        });

        if (!res.ok) {
          throw new Error(`Failed to refresh session: ${res.statusText}`);
        }

        const { client_secret } = await res.json();
        return client_secret;
      }

      // Create new session
      const res = await fetch('/api/chatkit/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!res.ok) {
        throw new Error(`Failed to create session: ${res.statusText}`);
      }

      const { client_secret } = await res.json();
      return client_secret;
    } catch (error) {
      console.error('ChatKit session error:', error);
      onError?.(error as Error);
      throw error;
    }
  }, [onError]);

  const { control } = useChatKit({
    api: {
      getClientSecret
    }
  });

  return (
    <div className="chatkit-container">
      <ChatKit
        control={control}
        className={className}
      />
    </div>
  );
};
```

**Acceptance Criteria**:
- [ ] Component initializes ChatKit with session management
- [ ] Handles session creation and refresh
- [ ] Error handling for API failures
- [ ] Responsive sizing with className prop

---

#### T107: Integrate TextSelectionContext with ChatKit
**Objective**: Connect Phase 6 text selection to ChatKit queries.

**Update**: `frontend/src/components/ChatBot/ChatKitWrapper.tsx`

```typescript
import { useTextSelection } from './TextSelectionContext';
import { useQueryMode } from './QueryModeToggle';

export const ChatKitWrapper: React.FC<ChatKitWrapperProps> = ({
  className,
  onError
}) => {
  // Get selection context from Phase 6
  const { selectionInfo } = useTextSelection();
  const { queryMode, setQueryMode } = useQueryMode();

  // ChatKit initialization (as before)
  const { control } = useChatKit({
    api: { getClientSecret },
    // Inject selection context into messages if in selected-text mode
    onBeforeSend: useCallback((message) => {
      if (queryMode === 'selected-text' && selectionInfo?.text) {
        return {
          ...message,
          metadata: {
            selectedText: selectionInfo.text,
            selectionContext: selectionInfo.context
          }
        };
      }
      return message;
    }, [queryMode, selectionInfo])
  });

  return (
    <div className="chatkit-container">
      {/* Phase 6 Query Mode Toggle */}
      {selectionInfo?.isValid && (
        <QueryModeToggle
          queryMode={queryMode}
          onModeChange={setQueryMode}
          selectedText={selectionInfo.text}
          compact={true}
        />
      )}

      <ChatKit control={control} className={className} />
    </div>
  );
};
```

**Acceptance Criteria**:
- [ ] Text selection from Phase 6 available to ChatKit
- [ ] Query mode toggle integrated in UI
- [ ] Selected text attached to messages as metadata
- [ ] Seamless switch between full-book and selected-text modes

---

#### T108: Create ChatBot Container Component
**Objective**: Build container that combines all chat components.

**Update**: `frontend/src/components/ChatBot/index.tsx`

```typescript
import React from 'react';
import { TextSelectionProvider } from './TextSelectionContext';
import { ChatKitWrapper } from './ChatKitWrapper';
import './styles.css';

export const ChatBot: React.FC = () => {
  const handleChatError = (error: Error) => {
    console.error('Chat error:', error);
    // TODO: Show user-friendly error message
  };

  return (
    <TextSelectionProvider>
      <div className="chatbot-container">
        <ChatKitWrapper
          className="h-full w-full"
          onError={handleChatError}
        />
      </div>
    </TextSelectionProvider>
  );
};

// Re-export all components
export { TextSelectionProvider, useTextSelection } from './TextSelectionContext';
export { QueryModeToggle, useQueryMode } from './QueryModeToggle';
export { ChatKitWrapper } from './ChatKitWrapper';
```

**Acceptance Criteria**:
- [ ] Container provides TextSelectionProvider context
- [ ] ChatKit and selection components properly integrated
- [ ] Error handling for chat failures
- [ ] Clean component API for embedding

---

#### T109: Add ChatBot to Documentation Pages
**Objective**: Embed ChatBot in Docusaurus documentation layout.

**New File**: `frontend/src/theme/Root.tsx`

```typescript
import React from 'react';
import { ChatBot } from '../components/ChatBot';

// Docusaurus Root wrapper for global components
export default function Root({ children }) {
  return (
    <>
      {children}
      <div className="chatbot-floating-container">
        <ChatBot />
      </div>
    </>
  );
}
```

**Update**: `frontend/src/components/ChatBot/styles.css`

```css
/* Floating chat container */
.chatbot-floating-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  overflow: hidden;
}

/* Responsive: hide on mobile, show button instead */
@media (max-width: 768px) {
  .chatbot-floating-container {
    bottom: 10px;
    right: 10px;
    width: 90vw;
    max-width: 400px;
  }
}

/* ChatKit customization */
.chatkit-container {
  font-family: var(--ifm-font-family-base);
}

/* Override ChatKit theme to match Docusaurus */
.chatkit-message {
  color: var(--ifm-color-content);
}

.chatkit-input {
  border-color: var(--ifm-color-emphasis-300);
}
```

**Acceptance Criteria**:
- [ ] ChatBot appears on all documentation pages
- [ ] Floating position in bottom-right corner
- [ ] Responsive design for mobile
- [ ] Matches Docusaurus theme

---

#### T110: Customize ChatKit Styling
**Objective**: Theme ChatKit to match the textbook design.

**Update**: `frontend/src/css/custom.css`

```css
/* ChatKit theme customization */
:root {
  --chatkit-primary: #4F46E5;
  --chatkit-primary-hover: #4338CA;
  --chatkit-background: #FFFFFF;
  --chatkit-border: #E5E7EB;
  --chatkit-text: #1F2937;
  --chatkit-text-secondary: #6B7280;
}

[data-theme='dark'] {
  --chatkit-primary: #7C3AED;
  --chatkit-primary-hover: #6D28D9;
  --chatkit-background: #1F2937;
  --chatkit-border: #374151;
  --chatkit-text: #F9FAFB;
  --chatkit-text-secondary: #9CA3AF;
}

/* Apply theme to ChatKit components */
.chatkit-container {
  --ck-color-primary: var(--chatkit-primary);
  --ck-color-primary-hover: var(--chatkit-primary-hover);
  --ck-color-background: var(--chatkit-background);
  --ck-color-border: var(--chatkit-border);
  --ck-color-text: var(--chatkit-text);
  --ck-color-text-secondary: var(--chatkit-text-secondary);
}

/* Source citations styling */
.chatkit-citation {
  background: var(--ifm-color-emphasis-100);
  border-left: 3px solid var(--chatkit-primary);
  padding: 8px 12px;
  margin: 8px 0;
  border-radius: 4px;
  font-size: 0.9em;
}

.chatkit-citation-title {
  font-weight: 600;
  color: var(--chatkit-primary);
  margin-bottom: 4px;
}

.chatkit-citation-text {
  color: var(--chatkit-text-secondary);
  font-style: italic;
}
```

**Acceptance Criteria**:
- [ ] ChatKit theme matches Docusaurus colors
- [ ] Dark mode support
- [ ] Custom citation styling
- [ ] Smooth animations and transitions

---

#### T111: Frontend Integration Testing
**Objective**: Test ChatKit integration and text selection flow.

**Test Scenarios**:

1. **Session Creation**
   - [ ] Chat initializes on page load
   - [ ] Session created successfully
   - [ ] No console errors

2. **Message Sending**
   - [ ] User can type and send messages
   - [ ] Messages appear in chat history
   - [ ] Streaming responses display correctly

3. **Text Selection Integration**
   - [ ] Highlight text in documentation
   - [ ] "Ask about selection" button appears
   - [ ] Query mode toggle works
   - [ ] Selected text included in query metadata

4. **Tool Execution**
   - [ ] `search_textbook` tool called automatically
   - [ ] Citations displayed with responses
   - [ ] Chapter references clickable
   - [ ] Confidence scores shown

5. **Error Handling**
   - [ ] Network errors display user-friendly message
   - [ ] Session refresh works after expiry
   - [ ] Invalid queries handled gracefully

6. **Responsive Design**
   - [ ] Chat works on desktop (1920x1080)
   - [ ] Chat works on tablet (768x1024)
   - [ ] Chat works on mobile (375x667)

**Acceptance Criteria**:
- [ ] All test scenarios pass
- [ ] No console errors or warnings
- [ ] Performance acceptable (<2s first message)

---

### Documentation Tasks (T112-T113)

#### T112: Update User Documentation
**Objective**: Document how to use the chat interface.

**New File**: `frontend/docs/using-the-chatbot.md`

```markdown
# Using the AI-Powered Chatbot

The Physical AI & Humanoid Robotics textbook includes an intelligent chatbot
powered by OpenAI's ChatKit framework. The bot can answer questions about
robotics concepts, provide code examples, and explain complex topics.

## Getting Started

1. **Open the Chat**: Click the chat icon in the bottom-right corner
2. **Ask a Question**: Type your question and press Enter
3. **View Response**: The bot will search the textbook and provide an answer with citations

## Features

### Full Textbook Search

Ask any question about topics covered in the textbook:

- "What is ROS 2 and how does it differ from ROS 1?"
- "Explain zero-moment point for bipedal walking"
- "How do I create a URDF model in ROS 2?"

### Context-Aware Queries

Highlight any passage from the textbook and ask about it:

1. Select text by clicking and dragging
2. Click "Ask about selection" button
3. Ask your question about the highlighted content

The bot will prioritize the selected text when answering.

### Source Citations

Every response includes citations showing:
- Which chapter the information came from
- Section type (concepts, algorithms, etc.)
- Relevance score
- Direct quotes from the textbook

Click citations to navigate to the source chapter.

## Tips for Better Results

1. **Be Specific**: "Explain the publish-subscribe pattern in ROS 2" is better than "How does ROS 2 work?"
2. **Use Context**: Highlight confusing passages before asking questions
3. **Follow Up**: Ask clarifying questions to dive deeper
4. **Request Examples**: Ask for code examples or practical applications

## Privacy

- Chat sessions expire after 1 hour of inactivity
- Conversations are not stored permanently
- Your queries help improve the system
```

**Acceptance Criteria**:
- [ ] User guide created and added to docs sidebar
- [ ] Screenshots included (to be added in Phase 9)
- [ ] Usage tips provided
- [ ] Privacy policy stated

---

#### T113: Update Developer Documentation
**Objective**: Document ChatKit integration for developers.

**Update**: `README.md`

```markdown
## Phase 7: ChatKit Integration

The textbook uses OpenAI's ChatKit framework for the AI-powered Q&A interface.

### Architecture

- **Frontend**: `@openai/chatkit-react` component with session management
- **Backend**: FastAPI endpoints for ChatKit session creation
- **RAG Integration**: `search_textbook` tool connects ChatKit to Phase 5 RAG service

### Setup

1. **Set OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY=sk-...
   ```

2. **Install Dependencies**:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt

   # Frontend
   cd frontend
   pnpm install
   ```

3. **Run Backend**:
   ```bash
   cd backend
   python -m uvicorn api.main:app --reload
   ```

4. **Run Frontend**:
   ```bash
   cd frontend
   pnpm start
   ```

5. **Test ChatBot**: Navigate to `http://localhost:3000` and open the chat

### Configuration

ChatKit settings in `backend/config/chatkit_config.py`:
- `model`: GPT-4 (default)
- `temperature`: 0.7
- `session_ttl`: 3600 seconds (1 hour)
- `tools`: search_textbook tool definition

### Customization

To customize the ChatKit theme, edit `frontend/src/css/custom.css`:

```css
:root {
  --chatkit-primary: #4F46E5;  /* Primary color */
  --chatkit-background: #FFFFFF;  /* Background */
}
```
```

**Acceptance Criteria**:
- [ ] Developer setup instructions provided
- [ ] Architecture diagram included
- [ ] Configuration options documented
- [ ] Troubleshooting section added

---

## Technical Considerations

### Performance

| Metric | Target | Strategy |
|--------|--------|----------|
| First message latency | <2s | Session pre-creation |
| Streaming response | Real-time | ChatKit built-in streaming |
| Tool execution | <1s | Efficient Qdrant retrieval |
| Session creation | <500ms | Async endpoint |

### Security

1. **API Key Protection**: Never expose OpenAI API key to frontend
2. **Session Isolation**: Each user gets unique session ID
3. **Rate Limiting**: Apply rate limits to session creation endpoint
4. **Input Validation**: Validate all user queries (max length, content filtering)

### Cost Management

- **Session TTL**: Limit session duration to reduce costs
- **Tool Call Limits**: Cap number of search_textbook calls per session
- **Model Selection**: Use GPT-4 for quality, consider GPT-3.5-turbo for cost savings
- **Caching**: Implement response caching for common queries

### Scalability

1. **Stateless Backend**: No session state stored on backend (ChatKit handles it)
2. **Horizontal Scaling**: Backend can scale independently
3. **CDN Delivery**: ChatKit JS served via CDN
4. **Lazy Loading**: ChatKit only loads when user opens chat

## Testing Strategy

### Unit Tests
- ChatKit session management (`test_chatkit_integration.py`)
- Tool handler logic (`test_chatkit_tools.py`)
- Configuration validation

### Integration Tests
- End-to-end message flow
- Tool execution with RAG service
- Session refresh flow
- Error handling

### Manual Testing
- User experience testing
- Text selection integration
- Citation display
- Mobile responsiveness

## Rollout Plan

### Phase 7.1: Backend Setup (T096-T103)
1. Install dependencies
2. Create session endpoints
3. Implement tool handlers
4. Test with curl/Postman

### Phase 7.2: Frontend Integration (T104-T111)
1. Install ChatKit React
2. Build wrapper component
3. Integrate text selection
4. Add to documentation pages
5. Style and theme

### Phase 7.3: Documentation (T112-T113)
1. User guide
2. Developer documentation
3. API reference

### Phase 7.4: Testing & Validation
1. Run all automated tests
2. Manual QA testing
3. Performance benchmarking
4. Security audit

## Success Metrics

- [ ] ChatKit initializes in <2s on page load
- [ ] Messages stream in real-time
- [ ] Text selection integration works seamlessly
- [ ] 95%+ of queries return relevant citations
- [ ] Zero critical bugs in production
- [ ] User satisfaction score >4.5/5

## Dependencies

**Requires**:
- Phase 5: RAG Backend (for search_textbook tool)
- Phase 6: Text Selection Context (for context-aware queries)

**Enables**:
- Phase 8: Deployment (production-ready chat interface)
- Phase 9: Polish (final UX improvements)

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| ChatKit API changes | High | Low | Pin SDK versions, monitor changelog |
| High API costs | Medium | Medium | Implement rate limiting, use caching |
| Session management issues | Medium | Low | Robust error handling, session refresh |
| Text selection breaks | Low | Medium | Thorough testing, fallback to full-book mode |

## Next Steps After Phase 7

1. **Phase 8**: Deploy to production with CI/CD pipeline
2. **Phase 9**: Polish UI/UX, add analytics, performance optimization
3. **Future**: Multi-language support, voice input, collaborative features

---

**Phase 7 Status**: 📋 **PLANNED** (Ready for implementation)

**Estimated Completion**: 2-3 days for full implementation and testing
