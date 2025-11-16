# 🚀 Deployment Architecture & Multi-User Concurrency Guide

## 📌 Context & Requirements

You're asking about:
1. **Multiple users** (2-5-10+) accessing agents simultaneously
2. **Shared vs Isolated** file/memory per user
3. **Persistent storage** (Database)
4. **Generated code storage** (Code repository)
5. **Long-term memory** across sessions
6. **Browser-based execution** (WebContainers)

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│                                                                 │
│  User 1    User 2    User 3    ...    User N                  │
│   (Tab)     (Tab)     (Tab)            (Tab)                    │
└────────────────────────────────────────┬────────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ↓                    ↓                    ↓
         ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
         │  WebContainer 1  │  │  WebContainer 2  │  │  WebContainer N  │
         │  (Browser Tab 1) │  │  (Browser Tab 2) │  │  (Browser Tab N) │
         │                  │  │                  │  │                  │
         │ Ephemeral Files  │  │ Ephemeral Files  │  │ Ephemeral Files  │
         │ (React + Vite)   │  │ (React + Vite)   │  │ (React + Vite)   │
         └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
                  │                    │                    │
                  └────────────────────┼────────────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ↓                  ↓                  ↓
        ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
        │  Python Backend  │  │  LangGraph Store │  │  PostgreSQL DB   │
        │  (Main Agent)    │  │  (Persistent Mem)│  │  (User Data)     │
        │                  │  │                  │  │                  │
        │ - Routes requests│  │ - /memories/     │  │ - User profiles  │
        │ - Coordinates    │  │   across threads │  │ - Code history   │
        │   agents         │  │                  │  │ - Generated files│
        │ - Manages users  │  │                  │  │ - Settings       │
        └──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## 🔑 Key Concepts

### 1. **Ephemeral Files** (Short-term, Per-User Session)
- **Location:** WebContainer (browser tab)
- **Lifetime:** During current session only
- **Examples:**
  - `/draft.md` - Working document
  - `/generated_code/hero.jsx` - Current component
  - `/temp_memory.json` - Session state

- **When Lost:** User closes tab or refreshes page

### 2. **Persistent Files** (Long-term, Per-User)
- **Location:** PostgreSQL Database (via LangGraph Store)
- **Path Format:** `/memories/*` in agent filesystem
- **Examples:**
  - `/memories/user_preferences.json` - User settings
  - `/memories/project_1/design_specs.json` - Project design
  - `/memories/project_1/components/hero.jsx` - Final code

- **When Persists:** Across all sessions, forever (until deleted)

### 3. **User Isolation**
Each user has their own:
- **Thread ID** (LangGraph concept)
- **Persistent memory namespace** (via Store)
- **Session ephemeral space** (WebContainer)

---

## 🏗️ System Architecture Breakdown

### A. Frontend Layer (React)

**File:** `frontend/pages/BuilderPage.jsx`

```jsx
// Each user gets a unique session
const [sessionId] = useState(generateUUID());
const [userId, setUserId] = useState(null);

// Send request to backend with user context
const startWebsiteBuilding = async (prompt) => {
  const response = await fetch('/api/build', {
    method: 'POST',
    body: JSON.stringify({
      userId,           // Which user
      sessionId,        // Which session
      prompt,
      timestamp: Date.now()
    })
  });
  
  // WebContainer renders the generated React code
  return response.json();
};
```

---

### B. Backend Layer (Python)

**File:** `src/services/agent_service.py` (Updated)

```python
# Multi-user agent management
class WebsiteBuilderService:
    
    def __init__(self):
        # Store for persistent memory across threads
        self.store = PostgresStore(
            connectionString=os.getenv("DATABASE_URL")
        )
        
        # Composite backend for ephemeral + persistent storage
        self.backend_factory = self._create_composite_backend
    
    def _create_composite_backend(self, config):
        """Create backend for a specific user session"""
        return CompositeBackend(
            StateBackend(config),  # Ephemeral (session-only)
            {
                "/memories/": StoreBackend(config)  # Persistent (user-specific)
            }
        )
    
    def build_website(self, user_id: str, prompt: str, session_id: str):
        """
        Build website for a specific user in a specific session
        
        Args:
            user_id: Database user ID
            prompt: User's website requirements
            session_id: Unique session identifier
        
        Returns:
            Generated React code + metadata
        """
        # Create thread config with user context
        config = {
            "configurable": {
                "thread_id": f"user_{user_id}_session_{session_id}",
                "user_id": user_id,
                "memory_namespace": f"memories/user_{user_id}"
            }
        }
        
        # Create agent with this user's context
        agent = self._create_agent_for_user(user_id, config)
        
        # Run agent - it will:
        # 1. Read from /memories/user_X/* (persistent memory)
        # 2. Write ephemeral files to session state
        # 3. Store final code in /memories/user_X/projects/
        result = agent.invoke({
            "messages": [{"role": "user", "content": prompt}]
        }, config)
        
        return result
```

---

### C. Storage Layer

#### **Ephemeral Storage (Per Session)**

**Lifetime:** Session only
**Where:** Agent state (StateBackend)
**Access:** Within same thread only

```python
# Only accessible in this session
/draft.md                 # Working draft
/temp_memory.json        # Session-only memory
/generated/hero.jsx      # Current work
```

---

#### **Persistent Storage (Per User)**

**Lifetime:** Forever
**Where:** PostgreSQL via LangGraph Store
**Access:** Any thread for same user

```python
# User 1's persistent data
/memories/user_1/preferences.json
/memories/user_1/projects/saas_landing/design_spec.json
/memories/user_1/projects/saas_landing/hero.jsx
/memories/user_1/projects/saas_landing/features.jsx
/memories/user_1/projects/saas_landing/METADATA.json

# User 2's persistent data (completely isolated)
/memories/user_2/preferences.json
/memories/user_2/projects/portfolio/design_spec.json
...
```

---

### D. Database Schema

#### **PostgreSQL Tables**

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  name VARCHAR,
  created_at TIMESTAMP,
  preferences JSONB  -- Color scheme, defaults, etc.
);

-- Projects table
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR,
  description TEXT,
  prompt TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Generated code table
CREATE TABLE generated_code (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  component_name VARCHAR,
  code TEXT,
  language VARCHAR,  -- 'jsx', 'css', etc.
  version INT,
  created_at TIMESTAMP,
  is_final BOOLEAN
);

-- LangGraph Store (handled by langfuse/langgraph)
-- Automatically manages /memories/* files per user
langgraph_checkpoints
  ├── Store persistent /memories/ files
  ├── Keyed by: namespace (user_id)
  └── Accessible across sessions
```

---

## 🔀 Multi-User Concurrency Handling

### Scenario: Users 1, 2, 3 Access Simultaneously

```
Time    User 1                    User 2                    User 3
────────────────────────────────────────────────────────────────────
T0      POST /api/build           
        sessionId: s1             
        userId: u1                
                                  POST /api/build
                                  sessionId: s2
                                  userId: u2
                                                            POST /api/build
                                                            sessionId: s3
                                                            userId: u3

T1      Backend creates:                                   Backend creates:
        thread_id: u1_s1          Backend creates:         thread_id: u3_s3
        memory_ns: u1             thread_id: u2_s2
                                  memory_ns: u2
                                                            
T2      Agent writes:            Agent writes:            Agent writes:
        /planning.json            /planning.json           /planning.json
        (u1 session)              (u2 session)             (u3 session)
        
T3      Reads from:              Reads from:              Reads from:
        /memories/user_1/*        /memories/user_2/*       /memories/user_3/*
        (completely isolated)     (completely isolated)    (completely isolated)

T4      Writes final code to:    Writes final code to:    Writes final code to:
        /memories/user_1/        /memories/user_2/        /memories/user_3/
        projects/proj1/          projects/proj2/          projects/proj3/
        hero.jsx                 hero.jsx                 hero.jsx
        
        (Different namespaces - NO CONFLICTS)
```

---

## 📊 Data Flow Diagram

### Single User's Project Lifecycle

```
┌─ User Input ─────────────────────────────────────────┐
│                                                       │
│  "Create SaaS landing page"                          │
└───────────────────────┬─────────────────────────────┘
                        │
                        ↓
        ┌───────────────────────────────┐
        │  Backend receives request      │
        │  user_id: u1                  │
        │  session_id: s1               │
        │  Creates thread config        │
        └───────────────┬───────────────┘
                        │
        ┌───────────────┴───────────────┐
        │ Agent starts execution        │
        └───────────────┬───────────────┘
                        │
        ┌───────────────┴────────────────────────┐
        │                                        │
        ↓                                        ↓
    ┌─────────────────┐              ┌──────────────────────┐
    │ Ephemeral Mem   │              │ Persistent Mem       │
    │ (StateBackend)  │              │ (StoreBackend)       │
    │                 │              │                      │
    │ Session: s1     │              │ /memories/user_1/    │
    │ /planning.json  │              │ /preferences.json    │
    │ /draft.md       │              │ /projects/...        │
    │ /temp.json      │              │                      │
    └────────┬────────┘              └──────────┬───────────┘
             │                                  │
             │  (Available ONLY in             │  (Available ALWAYS
             │   this session)                  │   for user_1)
             │                                  │
             └──────────────┬───────────────────┘
                            │
                            ↓
        ┌──────────────────────────────┐
        │ Generate React Components     │
        │ (One per component)           │
        └──────────────┬────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ↓                             ↓
    Code Critic              Visual Validator
    Validates syntax         Validates design match
    
    If OK → Approve          If OK → Approve
    If Not → Revise          If Not → Revise
        │                        │
        └────────────┬───────────┘
                     │
                     ↓
    ┌────────────────────────────────┐
    │ Store Final Code               │
    │ /memories/user_1/              │
    │ /projects/proj1/               │
    │ /hero.jsx                      │
    │ /features.jsx                  │
    │ /pricing.jsx                   │
    │ /METADATA.json                 │
    └────────────┬───────────────────┘
                 │
                 ↓
    ┌────────────────────────────────┐
    │ PostgreSQL Database            │
    │ - Code stored                  │
    │ - Project record updated       │
    │ - Audit trail recorded         │
    └────────────────────────────────┘
                 │
                 ↓
    ┌────────────────────────────────┐
    │ Return to Frontend             │
    │ Code ready for WebContainer    │
    └────────────────────────────────┘
```

---

## 💾 Data Storage Strategy

### 1. **Ephemeral Data** (Deleted After Session)
- Session-specific working files
- Temporary calculations
- Draft versions

**Storage:** Agent state (memory, not persisted)

### 2. **User Data** (Long-term Per-User)
- User preferences
- Project history
- Generated code

**Storage:** PostgreSQL Database

```sql
-- Example user data structure
{
  user_id: "u1",
  projects: [
    {
      id: "proj1",
      name: "SaaS Landing",
      created: "2025-11-16",
      components: [
        { name: "hero", version: 3, approved: true },
        { name: "features", version: 2, approved: true }
      ]
    }
  ]
}
```

### 3. **Agent Long-term Memory** (Via /memories/)
- Persistent files in PostgreSQL
- Namespace: Per-user
- Format: JSON files

```
/memories/user_1/
  ├── preferences.json       (User settings)
  ├── past_projects.json     (Project history)
  └── projects/
      ├── proj1/
      │   ├── design_spec.json
      │   ├── hero.jsx
      │   ├── features.jsx
      │   └── METADATA.json
      └── proj2/
          └── ...
```

---

## 🔐 Security & Isolation

### User Isolation Guarantees

```python
# User 1's agent cannot access User 2's data
User 1 agent:
  - thread_id: u1_s1
  - memory_namespace: u1
  - Can only read: /memories/user_1/*
  - CANNOT read: /memories/user_2/*
  
User 2 agent:
  - thread_id: u2_s2
  - memory_namespace: u2
  - Can only read: /memories/user_2/*
  - CANNOT read: /memories/user_1/*
```

### Verification

```python
# Backend enforces isolation
def get_agent_for_user(user_id, session_id):
    # Create isolated namespace
    namespace = f"user_{user_id}"
    
    config = {
        "configurable": {
            "thread_id": f"{namespace}_{session_id}",
            "namespace": namespace
        }
    }
    
    # Agent CANNOT escape this namespace
    # LangGraph Store enforces it
    return agent
```

---

## 🌐 WebContainer Integration

### How Generated Code Executes

```
1. Backend generates React code
   ↓
2. Store in PostgreSQL
   ↓
3. Return to Frontend
   ↓
4. Frontend loads in WebContainer
   ```jsx
   // WebContainer executes this
   import { WebContainer } from '@webcontainer/api';
   
   const webcontainer = await WebContainer.boot();
   
   await webcontainer.mount({
     'src/components/hero.jsx': { file: { contents: generatedCode } },
     'package.json': { ... },
     'vite.config.js': { ... }
   });
   
   await webcontainer.spawn('npm', ['install']);
   await webcontainer.spawn('npm', ['run', 'dev']);
   ```
   ↓
5. Live preview in iframe
   ↓
6. User can edit/iterate
```

---

## 📋 Implementation Checklist

### Phase 0: Setup (Before agent implementation)

- [ ] PostgreSQL database setup
  - [ ] Users table
  - [ ] Projects table
  - [ ] Generated code table

- [ ] LangGraph Store configuration
  - [ ] PostgresStore connection
  - [ ] User namespace mapping

- [ ] Backend API routes
  - [ ] POST /api/build
  - [ ] GET /api/projects/:userId
  - [ ] GET /api/project/:projectId

- [ ] Frontend setup
  - [ ] WebContainer integration
  - [ ] API client
  - [ ] Session management
  - [ ] Live preview iframe

### Phase 1: Website Builder Prompt

- [ ] Update agent prompt for website building
- [ ] Test single-user flow
- [ ] Verify persistence works

### Phase 2-7: Implement Agents

- [ ] Each agent implementation
- [ ] Test with /memories/* paths
- [ ] Verify isolation between users

---

## 🚀 Deployment Strategy

### Development
```
Backend: Local Python + PostgreSQL local
Frontend: React dev server
Storage: PostgreSQL on laptop
```

### Production
```
Backend: Python on Docker + Cloud PostgreSQL
Frontend: React build + CDN
Storage: Cloud PostgreSQL (AWS RDS / Google Cloud SQL)
Code execution: WebContainers (client-side)
```

---

## ❓ Answers to Your Questions

### Q1: How do multiple users access without conflicts?

**A:** Each user gets:
- Unique `thread_id`: `u1_s1`, `u2_s2`, `u3_s3`
- Isolated namespace: `/memories/user_1/`, `/memories/user_2/`
- Separate ephemeral session: Each browser tab has its own
- **Result:** No conflicts, completely isolated

---

### Q2: Same file or different files?

**A:** 
- **Ephemeral:** Different files per session (isolated)
- **Persistent:** Different `/memories/user_X/` directories per user
- **Database:** All users' data in same PostgreSQL, but namespaced
- **Result:** Logical isolation via namespacing

---

### Q3: Where does data storage happen?

**A:**

| Data Type | Location | When |
|-----------|----------|------|
| Session working files | Agent state (memory) | During session |
| Final generated code | PostgreSQL + `/memories/` | End of generation |
| User preferences | PostgreSQL | When saved |
| Project history | PostgreSQL | After each project |
| Audit trail | PostgreSQL logs | Continuously |

---

### Q4: How to structure the code?

**A:**
```
project/
├── backend/
│   ├── src/
│   │   ├── services/
│   │   │   ├── agent_service.py          (Agent creation)
│   │   │   └── storage_service.py        (DB access)
│   │   ├── routes/
│   │   │   └── builder.py                (API endpoints)
│   │   └── utils/
│   │       └── isolation.py              (User isolation)
│   └── database.py                       (DB config)
│
├── frontend/
│   ├── components/
│   │   ├── Builder/
│   │   ├── Preview/                      (WebContainer)
│   │   └── CodeEditor/
│   └── pages/
│       └── BuilderPage.jsx
│
└── docker-compose.yml                    (PostgreSQL)
```

---

## 🔄 Next Steps

1. **Understand the flow:** Read this document carefully
2. **Ask clarifications:** Any questions about isolation/storage?
3. **Start PHASE 0:** Setup PostgreSQL + API routes
4. **Then PHASE 1:** Update agent prompt for website builder
5. **Then PHASE 2+:** Implement agents with proper isolation

---

## 📚 Key Technologies

| Technology | Purpose | Implementation |
|------------|---------|-----------------|
| LangGraph | Agent orchestration | Python backend |
| PostgreSQL | Persistent storage | Cloud/Local DB |
| StoreBackend | Long-term memory | `/memories/*` paths |
| StateBackend | Ephemeral storage | Session-only |
| CompositeBackend | Hybrid storage | Both above combined |
| WebContainer | Code execution | Browser-based |
| React + Vite | Generated code | User-facing app |

---

**Ready to proceed with database setup and API design?** 🚀
