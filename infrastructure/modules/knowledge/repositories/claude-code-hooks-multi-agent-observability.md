# Claude Code Hooks Multi-Agent Observability - Complete Repository Extraction

## Repository Overview

**Repository**: <https://github.com/disler/claude-code-hooks-multi-agent-observability>  
**Purpose**: Real-time monitoring and visualization for Claude Code agents through comprehensive hook event tracking  
**Author**: IndyDevDan (disler)  
**Key Features**: Real-time dashboards, multi-agent monitoring, WebSocket streaming, SQLite persistence, Vue.js visualization

This system provides complete observability into Claude Code agent behavior by capturing, storing, and visualizing Claude Code Hook events in real-time. It enables monitoring of multiple concurrent agents with session tracking, event filtering, and live updates.

## Tutorial & Resources

**Video**: [Full Breakdown](https://youtu.be/9ijnN985O_c)

## Architecture Overview

```
Claude Agents → Hook Scripts → HTTP POST → Bun Server → SQLite → WebSocket → Vue Client
```

**Data Flow**:

1. **Event Generation**: Claude Code executes an action (tool use, notification, etc.)
2. **Hook Activation**: Corresponding hook script runs based on `settings.json` configuration
3. **Data Collection**: Hook script gathers context (tool name, inputs, outputs, session ID)
4. **Transmission**: `send_event.py` sends JSON payload to server via HTTP POST
5. **Server Processing**: Validates event structure, stores in SQLite, broadcasts to WebSocket clients
6. **Client Update**: Vue app receives event and updates timeline in real-time

## Setup Requirements

### Prerequisites

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - Anthropic's official CLI for Claude
- **[Astral uv](https://docs.astral.sh/uv/)** - Fast Python package manager (required for hook scripts)
- **[Bun](https://bun.sh/)**, **npm**, or **yarn** - For running the server and client
- **Anthropic API Key** - Set as `ANTHROPIC_API_KEY` environment variable
- **OpenAI API Key** (optional) - For multi-model support with just-prompt MCP tool
- **ElevenLabs API Key** (optional) - For audio features

## Project Structure

```
claude-code-hooks-multi-agent-observability/
│
├── apps/                    # Application components
│   ├── server/             # Bun TypeScript server
│   │   ├── src/
│   │   │   ├── index.ts    # Main server with HTTP/WebSocket endpoints
│   │   │   ├── db.ts       # SQLite database management & migrations
│   │   │   └── types.ts    # TypeScript interfaces
│   │   ├── package.json
│   │   └── events.db       # SQLite database (gitignored)
│   │
│   └── client/             # Vue 3 TypeScript client
│       ├── src/
│       │   ├── App.vue     # Main app with theme & WebSocket management
│       │   ├── components/
│       │   │   ├── EventTimeline.vue      # Event list with auto-scroll
│       │   │   ├── EventRow.vue           # Individual event display
│       │   │   ├── FilterPanel.vue        # Multi-select filters
│       │   │   ├── ChatTranscriptModal.vue # Chat history viewer
│       │   │   ├── StickScrollButton.vue  # Scroll control
│       │   │   └── LivePulseChart.vue     # Real-time activity chart
│       │   ├── composables/
│       │   │   ├── useWebSocket.ts        # WebSocket connection logic
│       │   │   ├── useEventColors.ts      # Color assignment system
│       │   │   ├── useChartData.ts        # Chart data aggregation
│       │   │   └── useEventEmojis.ts      # Event type emoji mapping
│       │   ├── utils/
│       │   │   └── chartRenderer.ts       # Canvas chart rendering
│       │   └── types.ts    # TypeScript interfaces
│       ├── .env.sample     # Environment configuration template
│       └── package.json
│
├── .claude/                # Claude Code integration
│   ├── hooks/             # Hook scripts (Python with uv)
│   │   ├── send_event.py  # Universal event sender
│   │   ├── pre_tool_use.py    # Tool validation & blocking
│   │   ├── post_tool_use.py   # Result logging
│   │   ├── notification.py    # User interaction events
│   │   ├── user_prompt_submit.py # User prompt logging & validation
│   │   ├── stop.py           # Session completion
│   │   └── subagent_stop.py  # Subagent completion
│   │
│   └── settings.json      # Hook configuration
│
├── scripts/               # Utility scripts
│   ├── start-system.sh   # Launch server & client
│   ├── reset-system.sh   # Stop all processes
│   └── test-system.sh    # System validation
│
└── logs/                 # Application logs (gitignored)
```

## Core Implementation - Universal Event Sender

### Universal Hook Script

**File**: `.claude/hooks/send_event.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "anthropic",
#     "python-dotenv",
# ]
# ///

"""
Multi-Agent Observability Hook Script
Sends Claude Code hook events to the observability server.
"""

import json
import sys
import os
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from utils.summarizer import generate_event_summary

def send_event_to_server(event_data, server_url='http://localhost:4000/events'):
    """Send event data to the observability server."""
    try:
        # Prepare the request
        req = urllib.request.Request(
            server_url,
            data=json.dumps(event_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Claude-Code-Hook/1.0'
            }
        )
        
        # Send the request
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                return True
            else:
                print(f"Server returned status: {response.status}", file=sys.stderr)
                return False
                
    except urllib.error.URLError as e:
        print(f"Failed to send event: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Send Claude Code hook events to observability server')
    parser.add_argument('--source-app', required=True, help='Source application name')
    parser.add_argument('--event-type', required=True, help='Hook event type (PreToolUse, PostToolUse, etc.)')
    parser.add_argument('--server-url', default='http://localhost:4000/events', help='Server URL')
    parser.add_argument('--add-chat', action='store_true', help='Include chat transcript if available')
    parser.add_argument('--summarize', action='store_true', help='Generate AI summary of the event')
    
    args = parser.parse_args()
    
    try:
        # Read hook data from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Prepare event data for server
    event_data = {
        'source_app': args.source_app,
        'session_id': input_data.get('session_id', 'unknown'),
        'hook_event_type': args.event_type,
        'payload': input_data,
        'timestamp': int(datetime.now().timestamp() * 1000)
    }
    
    # Handle --add-chat option
    if args.add_chat and 'transcript_path' in input_data:
        transcript_path = input_data['transcript_path']
        if os.path.exists(transcript_path):
            # Read .jsonl file and convert to JSON array
            chat_data = []
            try:
                with open(transcript_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                chat_data.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass  # Skip invalid lines
                
                # Add chat to event data
                event_data['chat'] = chat_data
            except Exception as e:
                print(f"Failed to read transcript: {e}", file=sys.stderr)
    
    # Generate summary if requested
    if args.summarize:
        summary = generate_event_summary(event_data)
        if summary:
            event_data['summary'] = summary
        # Continue even if summary generation fails
    
    # Send to server
    success = send_event_to_server(event_data, args.server_url)
    
    # Always exit with 0 to not block Claude Code operations
    sys.exit(0)

if __name__ == '__main__':
    main()
```

## Server Implementation - Bun TypeScript

**File**: `apps/server/src/index.ts`

```typescript
import { initDatabase, insertEvent, getFilterOptions, getRecentEvents } from './db';
import type { HookEvent } from './types';

// Initialize database
initDatabase();

// Store WebSocket clients
const wsClients = new Set<any>();

// Create Bun server with HTTP and WebSocket support
const server = Bun.serve({
  port: 4000,
  
  async fetch(req: Request) {
    const url = new URL(req.url);
    
    // Handle CORS
    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    // Handle preflight
    if (req.method === 'OPTIONS') {
      return new Response(null, { headers });
    }
    
    // POST /events - Receive new events
    if (url.pathname === '/events' && req.method === 'POST') {
      try {
        const event: HookEvent = await req.json();
        
        // Validate required fields
        if (!event.source_app || !event.session_id || !event.hook_event_type || !event.payload) {
          return new Response(JSON.stringify({ error: 'Missing required fields' }), {
            status: 400,
            headers: { ...headers, 'Content-Type': 'application/json' }
          });
        }
        
        // Insert event into database
        const savedEvent = insertEvent(event);
        
        // Broadcast to all WebSocket clients
        const message = JSON.stringify({ type: 'event', data: savedEvent });
        wsClients.forEach(client => {
          try {
            client.send(message);
          } catch (err) {
            // Client disconnected, remove from set
            wsClients.delete(client);
          }
        });
        
        return new Response(JSON.stringify(savedEvent), {
          headers: { ...headers, 'Content-Type': 'application/json' }
        });
      } catch (error) {
        console.error('Error processing event:', error);
        return new Response(JSON.stringify({ error: 'Invalid request' }), {
          status: 400,
          headers: { ...headers, 'Content-Type': 'application/json' }
        });
      }
    }
    
    // GET /events/filter-options - Get available filter options
    if (url.pathname === '/events/filter-options' && req.method === 'GET') {
      const options = getFilterOptions();
      return new Response(JSON.stringify(options), {
        headers: { ...headers, 'Content-Type': 'application/json' }
      });
    }
    
    // GET /events/recent - Get recent events
    if (url.pathname === '/events/recent' && req.method === 'GET') {
      const limit = parseInt(url.searchParams.get('limit') || '100');
      const events = getRecentEvents(limit);
      return new Response(JSON.stringify(events), {
        headers: { ...headers, 'Content-Type': 'application/json' }
      });
    }
    
    // WebSocket upgrade
    if (url.pathname === '/stream') {
      const success = server.upgrade(req);
      if (success) {
        return undefined;
      }
    }
    
    // Default response
    return new Response('Multi-Agent Observability Server', {
      headers: { ...headers, 'Content-Type': 'text/plain' }
    });
  },
  
  websocket: {
    open(ws) {
      console.log('WebSocket client connected');
      wsClients.add(ws);
      
      // Send recent events on connection
      const events = getRecentEvents(50);
      ws.send(JSON.stringify({ type: 'initial', data: events }));
    },
    
    message(ws, message) {
      // Handle any client messages if needed
      console.log('Received message:', message);
    },
    
    close(ws) {
      console.log('WebSocket client disconnected');
      wsClients.delete(ws);
    },
    
    error(ws, error) {
      console.error('WebSocket error:', error);
      wsClients.delete(ws);
    }
  }
});

console.log(`🚀 Server running on http://localhost:${server.port}`);
console.log(`📊 WebSocket endpoint: ws://localhost:${server.port}/stream`);
console.log(`📮 POST events to: http://localhost:${server.port}/events`);
```

## Client Implementation - Vue 3 Dashboard

**File**: `apps/client/src/App.vue`

```vue
<template>
  <div class="h-screen flex flex-col bg-[var(--theme-bg-secondary)]">
    <!-- Header with Primary Theme Colors -->
    <header class="bg-gradient-to-r from-[var(--theme-primary)] to-[var(--theme-primary-light)] shadow-lg border-b-2 border-[var(--theme-primary-dark)]">
      <div class="px-3 py-4 mobile:py-2 mobile:flex-col mobile:space-y-2 flex items-center justify-between">
        <!-- Title Section -->
        <div class="mobile:w-full mobile:text-center">
          <h1 class="text-2xl mobile:text-lg font-bold text-white drop-shadow-lg">
            Multi-Agent Observability
          </h1>
        </div>
        
        <!-- Connection Status -->
        <div class="mobile:w-full mobile:justify-center flex items-center space-x-1.5">
          <div v-if="isConnected" class="flex items-center space-x-1.5">
            <span class="relative flex h-3 w-3">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span class="text-base mobile:text-sm text-white font-semibold drop-shadow-md">Connected</span>
          </div>
          <div v-else class="flex items-center space-x-1.5">
            <span class="relative flex h-3 w-3">
              <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
            </span>
            <span class="text-base mobile:text-sm text-white font-semibold drop-shadow-md">Disconnected</span>
          </div>
        </div>
        
        <!-- Event Count and Theme Toggle -->
        <div class="mobile:w-full mobile:justify-center flex items-center space-x-2">
          <span class="text-base mobile:text-sm text-white font-semibold drop-shadow-md bg-[var(--theme-primary-dark)] px-3 py-1.5 rounded-full border border-white/30">
            {{ events.length }} events
          </span>
          
          <!-- Filters Toggle Button -->
          <button
            @click="showFilters = !showFilters"
            class="p-3 mobile:p-1.5 rounded-lg bg-white/20 hover:bg-white/30 transition-all duration-200 border border-white/30 hover:border-white/50 backdrop-blur-sm shadow-lg hover:shadow-xl"
            :title="showFilters ? 'Hide filters' : 'Show filters'"
          >
            <span class="text-2xl mobile:text-lg">📊</span>
          </button>
          
          <!-- Theme Manager Button -->
          <button
            @click="handleThemeManagerClick"
            class="p-3 mobile:p-1.5 rounded-lg bg-white/20 hover:bg-white/30 transition-all duration-200 border border-white/30 hover:border-white/50 backdrop-blur-sm shadow-lg hover:shadow-xl"
            title="Open theme manager"
          >
            <span class="text-2xl mobile:text-lg">🎨</span>
          </button>
        </div>
      </div>
    </header>
    
    <!-- Filters -->
    <FilterPanel
      v-if="showFilters"
      :filters="filters"
      @update:filters="filters = $event"
    />
    
    <!-- Live Pulse Chart -->
    <LivePulseChart
      :events="events"
      :filters="filters"
    />
    
    <!-- Timeline -->
    <EventTimeline
      :events="events"
      :filters="filters"
      v-model:stick-to-bottom="stickToBottom"
    />
    
    <!-- Stick to bottom button -->
    <StickScrollButton
      :stick-to-bottom="stickToBottom"
      @toggle="stickToBottom = !stickToBottom"
    />
    
    <!-- Error message -->
    <div
      v-if="error"
      class="fixed bottom-4 left-4 mobile:bottom-3 mobile:left-3 mobile:right-3 bg-red-100 border border-red-400 text-red-700 px-3 py-2 mobile:px-2 mobile:py-1.5 rounded mobile:text-xs"
    >
      {{ error }}
    </div>
    
    <!-- Theme Manager -->
    <ThemeManager 
      :is-open="showThemeManager"
      @close="showThemeManager = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useWebSocket } from './composables/useWebSocket';
import { useThemes } from './composables/useThemes';
import EventTimeline from './components/EventTimeline.vue';
import FilterPanel from './components/FilterPanel.vue';
import StickScrollButton from './components/StickScrollButton.vue';
import LivePulseChart from './components/LivePulseChart.vue';
import ThemeManager from './components/ThemeManager.vue';

// WebSocket connection
const { events, isConnected, error } = useWebSocket('ws://localhost:4000/stream');

// Theme management
const { state: themeState } = useThemes();

// Filters
const filters = ref({
  sourceApp: '',
  sessionId: '',
  eventType: ''
});

// UI state
const stickToBottom = ref(true);
const showThemeManager = ref(false);
const showFilters = ref(false);

// Computed properties
const isDark = computed(() => {
  return themeState.value.currentTheme === 'dark' || 
         (themeState.value.isCustomTheme && 
          themeState.value.customThemes.find(t => t.id === themeState.value.currentTheme)?.name.includes('dark'));
});

// Debug handler for theme manager
const handleThemeManagerClick = () => {
  console.log('Theme manager button clicked!');
  showThemeManager.value = true;
};
</script>
```

## Event Types & Visualization System

### Event Type Mapping

| Event Type       | Emoji | Purpose                | Color Coding  | Special Display                   |
| ---------------- | ----- | ---------------------- | ------------- | --------------------------------- |
| PreToolUse       | 🔧     | Before tool execution  | Session-based | Tool name & details               |
| PostToolUse      | ✅     | After tool completion  | Session-based | Tool name & results               |
| Notification     | 🔔     | User interactions      | Session-based | Notification message              |
| Stop             | 🛑     | Response completion    | Session-based | Summary & chat transcript         |
| SubagentStop     | 👥     | Subagent finished      | Session-based | Subagent details                  |
| PreCompact       | 📦     | Context compaction     | Session-based | Compaction details                |
| UserPromptSubmit | 💬     | User prompt submission | Session-based | Prompt: _"user message"_ (italic) |

### UserPromptSubmit Event (v1.0.54+)

The `UserPromptSubmit` hook captures every user prompt before Claude processes it. In the UI:

- Displays as `Prompt: "user's message"` in italic text
- Shows the actual prompt content inline (truncated to 100 chars)
- Summary appears on the right side when AI summarization is enabled
- Useful for tracking user intentions and conversation flow

## Configuration & Integration

### Hook Configuration

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "uv run .claude/hooks/pre_tool_use.py"
        },
        {
          "type": "command",
          "command": "uv run .claude/hooks/send_event.py --source-app YOUR_PROJECT_NAME --event-type PreToolUse --summarize"
        }
      ]
    }],
    "PostToolUse": [{
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "uv run .claude/hooks/post_tool_use.py"
        },
        {
          "type": "command",
          "command": "uv run .claude/hooks/send_event.py --source-app YOUR_PROJECT_NAME --event-type PostToolUse --summarize"
        }
      ]
    }],
    "UserPromptSubmit": [{
      "hooks": [
        {
          "type": "command",
          "command": "uv run .claude/hooks/user_prompt_submit.py --log-only"
        },
        {
          "type": "command",
          "command": "uv run .claude/hooks/send_event.py --source-app YOUR_PROJECT_NAME --event-type UserPromptSubmit --summarize"
        }
      ]
    }]
    // ... similar patterns for other events
  }
}
```

### Environment Configuration

**Application Root** (`.env` file):

- `ANTHROPIC_API_KEY` – Anthropic Claude API key (required)
- `ENGINEER_NAME` – Your name (for logging/identification)
- `GEMINI_API_KEY` – Google Gemini API key (optional)
- `OPENAI_API_KEY` – OpenAI API key (optional)
- `ELEVEN_API_KEY` – ElevenLabs API key (optional)

**Client** (`.env` file in `apps/client/.env`):

- `VITE_MAX_EVENTS_TO_DISPLAY=100` – Maximum events to show

## Quick Start & Usage

### System Setup

```bash
# 1. Start both server and client
./scripts/start-system.sh

# 2. Open http://localhost:5173 in your browser

# 3. Open Claude Code and run commands:
claude -p "Run git ls-files to understand the codebase."

# 4. Watch events stream in the client

# 5. Copy the .claude folder to other projects
cp -R .claude <target_directory>
```

### Integration for New Projects

1. Copy the event sender:

```bash
cp .claude/hooks/send_event.py YOUR_PROJECT/.claude/hooks/
```

2. Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": ".*",
      "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/send_event.py --source-app YOUR_APP --event-type PreToolUse"
      }]
    }]
  }
}
```

## Technical Features

### Real-Time Visualization

- **Visual Design**: Dual-color system with app colors (left border) + session colors (second border)
- **Gradient Indicators**: Visual distinction between different sessions and apps
- **Dark/Light Theme**: Support with smooth theme transitions
- **Responsive Layout**: Mobile-friendly design with smooth animations

### Advanced Dashboard Features

- **Real-time WebSocket Updates**: Live event streaming
- **Multi-criteria Filtering**: Filter by app, session, event type
- **Live Pulse Chart**: Session-colored bars with event type indicators
- **Time Range Selection**: 1m, 3m, 5m with appropriate data aggregation
- **Chat Transcript Viewer**: Syntax highlighting for conversation history
- **Auto-scroll with Override**: Stick to bottom with manual control
- **Event Limiting**: Configurable via `VITE_MAX_EVENTS_TO_DISPLAY`

### Live Pulse Chart Features

- **Canvas-based Visualization**: Real-time rendering with smooth performance
- **Session-specific Colors**: Each bar colored by session ID
- **Event Type Emojis**: Displayed on bars for quick identification
- **Smooth Animations**: Glow effects and transitions
- **Filter Responsive**: Updates in real-time based on active filters

## Database & Persistence

### SQLite Database Features

- **WAL Mode**: Concurrent access support
- **Automatic Migrations**: Schema versioning and updates
- **Event Validation**: Data integrity checks
- **Chat Transcript Storage**: Full conversation history
- **Filter Optimization**: Indexed queries for fast filtering

### API Endpoints

**Server** (Port 4000):

- `POST /events` - Receive events from agents
- `GET /events/recent` - Paginated event retrieval with filtering
- `GET /events/filter-options` - Available filter values
- `WS /stream` - Real-time event broadcasting

**Client** (Port 5173):

- Vite development server with hot reloading
- Theme management system
- Real-time dashboard interface

## Security & Reliability

### Security Features

- **Command Blocking**: Dangerous commands (`rm -rf`, etc.) blocked
- **File Access Control**: Prevents access to sensitive files (`.env`, private keys)
- **Input Validation**: All inputs validated before execution
- **Graceful Error Handling**: No interruption to Claude Code operations

### Reliability Features

- **Automatic Reconnection**: WebSocket reconnection on failures
- **Error Recovery**: Graceful handling of server disconnections
- **Data Persistence**: SQLite ensures no data loss
- **Hook Failure Isolation**: Failed hooks don't break Claude Code execution

## Troubleshooting

### Hook Scripts Not Working

If hook scripts aren't executing properly, it might be due to relative paths in your `.claude/settings.json`. Use the custom slash command:

```bash
# In Claude Code, run:
/convert_paths_absolute
```

This command will:

- Find all relative paths in hook command scripts
- Convert them to absolute paths based on current working directory
- Create backup of original settings.json
- Show exactly what changes were made

## Technical Stack

### Backend

- **Runtime**: Bun (ultra-fast JavaScript runtime)
- **Language**: TypeScript
- **Database**: SQLite with WAL mode
- **WebSocket**: Built-in Bun WebSocket support
- **API**: RESTful HTTP endpoints

### Frontend

- **Framework**: Vue 3 with Composition API
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Canvas-based custom rendering
- **State Management**: Vue 3 reactive system

### Hook System

- **Language**: Python 3.8+
- **Package Manager**: Astral UV
- **Dependencies**: Anthropic SDK, python-dotenv
- **Communication**: HTTP POST to server
- **Format**: JSON event payloads

## Advanced Integration Patterns

### Multi-Project Monitoring

```bash
# Monitor multiple projects simultaneously
# Project A
cp -R .claude /path/to/project-a/
# Update source-app to "project-a" in settings.json

# Project B  
cp -R .claude /path/to/project-b/
# Update source-app to "project-b" in settings.json

# All projects send to same observability server
# Dashboard shows events from all projects with color coding
```

### Event Summarization

```python
# Enable AI summarization of events
"uv run .claude/hooks/send_event.py --source-app myapp --event-type PreToolUse --summarize"

# Summary appears in dashboard for better understanding
# Powered by Anthropic or OpenAI APIs
```

### Chat History Integration

```python
# Include full conversation transcripts
"uv run .claude/hooks/send_event.py --source-app myapp --event-type Stop --add-chat"

# View full conversation history in dashboard
# Syntax highlighted for better readability
```

## Extensions & Customization

### Custom Event Types

- Add new hook types in Claude Code settings
- Extend the event sender with new event types
- Update dashboard to handle new event visualization

### Theme System

- Built-in dark/light themes
- Custom theme creation and management
- Theme import/export functionality
- Session-based color assignments

### Filter Extensions

- Multi-dimensional filtering
- Time-range based filtering
- Custom filter criteria
- Filter state persistence

## Performance Characteristics

### Scalability

- **Database**: SQLite handles thousands of events efficiently
- **WebSocket**: Bun's native WebSocket support for real-time updates
- **Frontend**: Vue 3 reactivity with efficient re-rendering
- **Memory**: Configurable event limits prevent memory bloat

### Real-Time Performance

- **Event Processing**: Sub-millisecond event ingestion
- **WebSocket Broadcasting**: Instant event distribution to clients
- **UI Updates**: Smooth animations with 60fps performance
- **Chart Rendering**: Canvas-based rendering for optimal performance

## Resources & References

- **Tutorial Video**: [Full Breakdown](https://youtu.be/9ijnN985O_c)
- **Related**: [Claude Code Hooks Mastery](https://github.com/disler/claude-code-hooks-mastery)
- **Author Channel**: [IndyDevDan YouTube](https://www.youtube.com/@indydevdan)
- **AI Coding Principles**: [Principled AI Coding](https://agenticengineer.com/principled-ai-coding?y=cchookobvs)
- **Claude Code Documentation**: [Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)

Built by [IndyDevDan](https://www.youtube.com/@indydevdan) demonstrating comprehensive observability and monitoring for Claude Code multi-agent systems.
