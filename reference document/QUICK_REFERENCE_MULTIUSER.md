# 🎯 Quick Reference: Multi-User Architecture

## The Simple Answer to Your Questions

### Q: How do 2-5-10 users access without conflicts?

**A: Thread IDs + Namespacing**

```
User 1: thread_id = "u1_session_abc" → /memories/user_1/*
User 2: thread_id = "u2_session_def" → /memories/user_2/*
User 3: thread_id = "u3_session_ghi" → /memories/user_3/*

Each has completely isolated namespace
No conflicts = completely separate data
```

---

### Q: Same file or different files?

**A: Different files, same database**

```
All users' data in PostgreSQL
But in separate namespaces

    PostgreSQL Database
    ├── /memories/user_1/    ← User 1's data
    ├── /memories/user_2/    ← User 2's data  
    ├── /memories/user_3/    ← User 3's data
    └── ...

Similar to folders in Google Drive:
- All in same cloud
- But your folder ≠ my folder
```

---

### Q: Where does storage happen?

**A: Two places**

```
SESSION STORAGE (Disappears after)
└─ Browser WebContainer (ephemeral files)
   └─ Only for current session

PERMANENT STORAGE (Forever)
└─ PostgreSQL Database
   ├─ Generated code (React components)
   ├─ User preferences
   ├─ Project history
   └─ /memories/ (persistent agent memory)
```

---

### Q: How to structure code?

**A: Three layers**

```
LAYER 1: Frontend (React)
│
├─ What it does: User interface + WebContainer preview
├─ Location: Browser (client-side)
├─ Lives in: WebContainer (in-browser Node.js)
└─ Files: Generated React code

        ↓ (HTTP request)

LAYER 2: Backend (Python)
│
├─ What it does: Coordinates AI agents, manages users
├─ Location: Cloud server
├─ Lives in: Docker container or VM
└─ Files: Agent code, API routes

        ↓ (Read/Write)

LAYER 3: Database (PostgreSQL)
│
├─ What it does: Stores all permanent data
├─ Location: Managed database (AWS RDS / Google Cloud)
├─ Lives in: Cloud database
└─ Files: User data, generated code, memories
```

---

## Code Example: User Isolation in Practice

### Before: No isolation (BAD)
```python
# Both users modify same memory
agent.invoke({"prompt": "Build website"})
# User 1 and User 2 might read each other's /draft.md ❌
```

### After: With isolation (GOOD)
```python
# Each user has isolated namespace
user_id = "u1"
session_id = "abc123"

config = {
    "configurable": {
        "thread_id": f"user_{user_id}_session_{session_id}",
        "namespace": f"user_{user_id}"
    }
}

agent.invoke(
    {"prompt": "Build website"},
    config
)

# User 1 can ONLY access /memories/user_1/*
# User 2 can ONLY access /memories/user_2/*
# Completely isolated ✅
```

---

## The "Memory File" Explained

### What is it?
A JSON file that acts as:
- **State container:** Where agents store current progress
- **Communication channel:** How agents pass data to each other
- **Audit trail:** Who did what and when

### Where does it live?
```
EPHEMERAL (Session only)
└─ /planning.json         ← Dies when session ends
└─ /draft.md              ← Dies when session ends

PERSISTENT (Forever, per user)
└─ /memories/user_1/project_1/
   └─ design_spec.json    ← Lives forever
   └─ hero.jsx            ← Lives forever
```

### Is it virtual or real?
**Both!**
- Virtual (in-memory) during session = fast
- Real (database) after session = permanent

---

## Multi-User Flow Example

### Scenario: 3 users building websites simultaneously

```
TIME  USER 1                USER 2                USER 3
────  ──────────────────    ──────────────────    ──────────────────
 0    Send request          
      "Build SaaS site"     
      
 1                          Send request
                            "Build Portfolio"
                            
 2                                              Send request
                                                "Build Blog"
                                                
 3    Backend creates       Backend creates      Backend creates
      thread: u1_session1   thread: u2_session2  thread: u3_session3
      
 4    Agent starts          Agent starts         Agent starts
      /memories/user_1/     /memories/user_2/    /memories/user_3/
      
 5    Planning phase        Planning phase       Planning phase
      ✓ Isolated            ✓ Isolated           ✓ Isolated
      
 6    Component search      Component search     Component search
      ✓ Isolated            ✓ Isolated           ✓ Isolated
      
 7    Design phase          Design phase         Design phase
      ✓ Isolated            ✓ Isolated           ✓ Isolated
      
 8    Code generation       Code generation      Code generation
      ✓ Isolated            ✓ Isolated           ✓ Isolated
      
 9    Store to DB           Store to DB          Store to DB
      user_1 data           user_2 data          user_3 data
      ✓ Isolated            ✓ Isolated           ✓ Isolated
      
10    Return to frontend    Return to frontend   Return to frontend
      User 1 sees their     User 2 sees their    User 3 sees their
      generated code        generated code       generated code
```

**Result:** Zero conflicts, all 3 users work independently

---

## Storage Locations Reference

```
┌─────────────────────────────────────────────────┐
│ WebContainer (Browser - Ephemeral)              │
│                                                 │
│ /node_modules/                                  │
│ /src/components/hero.jsx  ← Generated code      │
│ /src/components/features.jsx                    │
│ /public/                                        │
│ /package.json                                   │
│ /vite.config.js                                 │
│                                                 │
│ Note: Deleted when tab closes ❌                │
└────────────────┬────────────────────────────────┘
                 │ Download/Execute
                 ↓
┌─────────────────────────────────────────────────┐
│ PostgreSQL Database (Cloud - Permanent)         │
│                                                 │
│ users table                                     │
│ ├── id: u1, u2, u3                             │
│ ├── email                                       │
│ └── preferences                                 │
│                                                 │
│ projects table                                  │
│ ├── id                                          │
│ ├── user_id (u1, u2, or u3)                    │
│ ├── name                                        │
│ └── created_at                                  │
│                                                 │
│ generated_code table                            │
│ ├── id                                          │
│ ├── project_id                                  │
│ ├── component_name (hero, features, etc)       │
│ ├── code (React JSX)                           │
│ └── version                                     │
│                                                 │
│ LangGraph Store (for /memories/)               │
│ ├── namespace: user_1                          │
│ │   └── /memories/user_1/project_1/design.json│
│ ├── namespace: user_2                          │
│ │   └── /memories/user_2/project_1/design.json│
│ └── namespace: user_3                          │
│     └── /memories/user_3/project_1/design.json│
│                                                 │
│ Note: Persists forever ✓                       │
└─────────────────────────────────────────────────┘
```

---

## The Complete Data Journey

```
1. User types prompt in browser
   "Create SaaS landing page"
   
   ↓
   
2. Frontend sends to backend with user context
   POST /api/build
   {
     userId: "u1",
     sessionId: "abc123",
     prompt: "Create SaaS landing page"
   }
   
   ↓
   
3. Backend creates isolated agent
   thread_id: "u1_abc123"
   namespace: "user_1"
   
   ↓
   
4. Agent executes (planner → design → generation → validation)
   - Reads from: /memories/user_1/*
   - Writes ephemeral to: session state
   - Writes persistent to: /memories/user_1/project_1/*
   
   ↓
   
5. Backend stores final code in PostgreSQL
   INSERT INTO generated_code VALUES (
     id: 'hero_1',
     project_id: 'proj_1',
     component_name: 'hero',
     code: 'export default function Hero() { ... }',
     user_id: 'u1'
   )
   
   ↓
   
6. Backend returns code to frontend
   {
     status: 'success',
     code: {
       hero: '...',
       features: '...',
       pricing: '...'
     }
   }
   
   ↓
   
7. Frontend loads in WebContainer
   - Mounts the files
   - Runs `npm install`
   - Runs `npm run dev`
   - Shows live preview in iframe
   
   ↓
   
8. User sees rendered website
   - Can preview in browser
   - Can edit if needed
   - Can download/deploy
```

---

## Key Principles

```
✅ DO: Each user has own thread + namespace
❌ DON'T: Share namespace between users

✅ DO: Use thread_id for isolation
❌ DON'T: Use global memory

✅ DO: Store code in PostgreSQL
❌ DON'T: Store in just memory

✅ DO: Use /memories/user_X/ pattern
❌ DON'T: Use /memories/ without user prefix

✅ DO: Validate user_id on every request
❌ DON'T: Trust user_id from frontend alone

✅ DO: Separate ephemeral and persistent data
❌ DON'T: Mix session and permanent data
```

---

## Before You Code

**Ask yourself:**
1. Which user am I serving? (user_id)
2. Is this data temporary or permanent?
3. Should other users see this data? (NO!)
4. Where should this be stored? (DB or session)
5. Do I have proper isolation in place?

---

**Next Step:** Ready to implement PHASE 0 (Database setup)?

Or do you need more clarification on any part? 🎯
