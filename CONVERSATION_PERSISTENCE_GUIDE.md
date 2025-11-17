# 💬 Conversation Persistence Guide

## Overview

Luna Website Builder now includes **automatic conversation persistence**. Every interaction with the CLI is saved to `conversation.json`, enabling:

- **Continuous conversations** across multiple CLI sessions
- **Full conversation history** sent to the LLM for better context
- **Conversation management** commands (stats, export, clear)
- **No manual tracking** required—everything is automatic

---

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI (cli.py)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. User inputs prompt                                │  │
│  │  2. ConversationManager.add_user_message(prompt)      │  │
│  │  3. Load full history from conversation.json          │  │
│  │  4. Send full history to LLM                          │  │
│  │  5. Get LLM response                                  │  │
│  │  6. ConversationManager.add_assistant_message(resp)   │  │
│  │  7. Save to conversation.json                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ↓
              ┌───────────────────────┐
              │  conversation.json    │
              │  {                    │
              │    "messages": [      │
              │      {                │
              │        "role": "user",│
              │        "content": "...",│
              │        "timestamp": "..."│
              │      },               │
              │      {                │
              │        "role": "assistant",│
              │        "content": "...",│
              │        "timestamp": "..."│
              │      }                │
              │    ],                 │
              │    "last_updated": "...",│
              │    "total_messages": 2│
              │  }                    │
              └───────────────────────┘
```

### File Structure

**`conversation.json`** (auto-generated):
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Build me a portfolio website",
      "timestamp": "2024-01-15T10:30:00.123456"
    },
    {
      "role": "assistant",
      "content": "I'll help you build a portfolio website...",
      "timestamp": "2024-01-15T10:30:15.654321"
    }
  ],
  "last_updated": "2024-01-15T10:30:15.654321",
  "total_messages": 2
}
```

### Key Features

1. **Automatic Persistence**
   - Every message is automatically saved
   - No manual intervention required
   - Works in both interactive and prompt modes

2. **Full History Context**
   - Every LLM call includes complete conversation history
   - Better context awareness for multi-turn conversations
   - Agents remember previous requests and responses

3. **Conversation Management**
   - View statistics (message counts)
   - Export conversations to readable text files
   - Clear history to start fresh

---

## Usage

### Interactive Mode (Default)

```bash
python luna.py
# or
python luna.py chat
```

**Features:**
- Type prompts naturally
- Full conversation history maintained
- Special commands available:
  - `exit` / `quit` / `q` - Exit the session
  - `clear` - Clear conversation history
  - `stats` - Show conversation statistics

**Example Session:**
```
🎨 Luna Website Builder - Multi-Agent System
============================================================

💬 Continuing conversation with 4 existing messages

🤖 You: Add a contact form to the homepage

🔄 Agent: Thinking...

✅ Agent: I'll add a contact form component to the homepage...
```

---

### Prompt Mode (Single Command)

```bash
python luna.py prompt "Build me a portfolio website"
```

**Features:**
- Execute single prompts
- Continues from previous conversation
- Full history sent to LLM
- Useful for scripting and automation

**Example:**
```bash
# First prompt
python luna.py prompt "Build me a portfolio website"

# Follow-up prompt (has context from first)
python luna.py prompt "Add a dark mode toggle"
```

---

### Conversation Management Commands

#### 1. Show Statistics

```bash
python luna.py stats
```

**Output:**
```
============================================================
          📊 Conversation Statistics
============================================================

  Total messages: 8
  User messages: 4
  Assistant messages: 4
```

#### 2. Export Conversation

```bash
# Export to default file (conversation_export.txt)
python luna.py export

# Export to custom file
python luna.py export my_conversation.txt
```

**Exported Format:**
```
================================================================================
Luna Website Builder - Conversation History
================================================================================

[1] 🤖 You (2024-01-15T10:30:00.123456):
Build me a portfolio website
--------------------------------------------------------------------------------

[2] ✅ Luna (2024-01-15T10:30:15.654321):
I'll help you build a portfolio website...
--------------------------------------------------------------------------------

================================================================================
Total Messages: 2
User Messages: 1
Assistant Messages: 1
================================================================================
```

#### 3. Clear History

```bash
python luna.py clear
```

**Interactive Confirmation:**
```
⚠️  Are you sure you want to clear conversation history? (yes/no): yes
✅ Conversation history cleared.
```

---

## ConversationManager API

For developers who want to use the conversation manager programmatically:

```python
from src.utils.conversation_manager import get_conversation_manager

# Get singleton instance
conversation_mgr = get_conversation_manager()

# Add messages
conversation_mgr.add_user_message("Hello!")
conversation_mgr.add_assistant_message("Hi there!")

# Get messages for LLM (without timestamps)
messages = conversation_mgr.get_messages_for_llm()
# Returns: [{"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hi there!"}]

# Get statistics
stats = conversation_mgr.get_conversation_stats()
# Returns: {"user_count": 1, "assistant_count": 1, "total_count": 2}

# Export conversation
conversation_mgr.export_conversation("output.txt")

# Clear history
conversation_mgr.clear_conversation()
```

---

## Implementation Details

### File: `src/utils/conversation_manager.py`

**Key Methods:**

| Method | Description |
|--------|-------------|
| `__init__(conversation_file)` | Initialize manager with file path |
| `add_user_message(content)` | Add user message and save |
| `add_assistant_message(content)` | Add assistant message and save |
| `get_messages_for_llm()` | Get messages formatted for LLM (no timestamps) |
| `get_conversation_stats()` | Get message counts |
| `export_conversation(output_file)` | Export to readable text file |
| `clear_conversation()` | Clear all history |

**Singleton Pattern:**
```python
# Global instance management
_conversation_manager = None

def get_conversation_manager(conversation_file="conversation.json"):
    global _conversation_manager
    if _conversation_manager is None:
        _conversation_manager = ConversationManager(conversation_file)
    return _conversation_manager
```

### File: `cli/cli.py`

**Integration Points:**

1. **Interactive Mode:**
   - Initialize conversation manager on startup
   - Add user message before LLM call
   - Add assistant message after LLM response
   - Support in-chat commands (clear, stats)

2. **Prompt Mode:**
   - Initialize conversation manager
   - Add user prompt to history
   - Send full history to LLM
   - Add response to history

3. **CLI Commands:**
   - `export` - Export conversation to file
   - `clear` - Clear conversation history
   - `stats` - Show conversation statistics

---

## Best Practices

### 1. When to Clear History

Clear conversation history when:
- Starting a completely new project
- Switching to a different type of website
- Previous context is no longer relevant
- conversation.json gets too large (>100 messages)

### 2. Exporting Conversations

Export conversations to:
- Document the website building process
- Share requirements with team members
- Create project documentation
- Review agent responses for quality

### 3. Using Prompt Mode

Use prompt mode for:
- Scripting and automation
- CI/CD pipelines
- Quick single requests
- Testing agent responses

Use interactive mode for:
- Iterative website development
- Complex multi-step projects
- Real-time collaboration
- Exploratory design sessions

---

## Error Handling

The conversation manager handles various error scenarios:

### 1. Corrupted JSON File

```
⚠️  Conversation file is corrupted. Starting fresh.
```

**Recovery:** Automatically starts with empty history

### 2. File Permission Issues

```
⚠️  Error saving conversation: [Errno 13] Permission denied
```

**Solution:** Check file permissions for `conversation.json`

### 3. Large File Size

If `conversation.json` becomes very large (>10MB):
- Export the conversation
- Clear the history
- Start fresh

---

## Advanced Usage

### Custom Conversation File Location

```python
from src.utils.conversation_manager import ConversationManager

# Use custom file location
custom_mgr = ConversationManager("/path/to/my_conversation.json")
```

### Multiple Conversation Threads

```python
# Project A conversation
project_a_mgr = ConversationManager("project_a_conversation.json")

# Project B conversation
project_b_mgr = ConversationManager("project_b_conversation.json")
```

### Programmatic Conversation Export

```python
from src.utils.conversation_manager import get_conversation_manager

conversation_mgr = get_conversation_manager()

# Export after every 10 messages
stats = conversation_mgr.get_conversation_stats()
if stats['total_count'] % 10 == 0:
    conversation_mgr.export_conversation(f"backup_{stats['total_count']}.txt")
```

---

## Troubleshooting

### Problem: Conversation not persisting

**Check:**
1. File permissions for writing `conversation.json`
2. Disk space availability
3. No errors in console output

**Solution:**
```bash
# Check file exists and has correct permissions
ls -la conversation.json

# Remove and recreate if corrupted
rm conversation.json
python luna.py
```

### Problem: Too much context sent to LLM

**Symptoms:**
- Slow response times
- Token limit errors
- High API costs

**Solution:**
```bash
# Clear history periodically
python luna.py clear

# Export before clearing
python luna.py export backup.txt
python luna.py clear
```

### Problem: Can't find conversation.json

**Location:** The file is created in the current working directory where you run `python luna.py`

**Solution:**
```bash
# Check current directory
pwd

# List files
ls -la conversation.json
```

---

## Future Enhancements

Potential improvements for conversation persistence:

1. **Conversation Branching**
   - Multiple conversation threads per project
   - Switch between threads
   - Merge conversations

2. **Smart Context Pruning**
   - Automatically summarize old messages
   - Keep only relevant context
   - Reduce token usage

3. **Conversation Search**
   - Search through message history
   - Filter by date/role/keywords
   - Find specific interactions

4. **Cloud Sync**
   - Sync conversations across devices
   - Collaborate with team members
   - Cloud backup and restore

5. **Conversation Analytics**
   - Token usage per conversation
   - Response time metrics
   - Agent performance insights

---

## Summary

✅ **Automatic conversation persistence** - No manual tracking needed  
✅ **Full context awareness** - LLM gets complete conversation history  
✅ **Easy management** - Simple commands for stats, export, clear  
✅ **Multi-session support** - Continue conversations across CLI sessions  
✅ **Robust error handling** - Graceful recovery from file issues  
✅ **Developer-friendly API** - Easy to extend and customize  

The conversation persistence system ensures Luna Website Builder maintains context across all interactions, providing a seamless multi-turn conversation experience for building complex websites.
