# 🎯 AI Website Builder - Understanding & Planning Document

## 📌 GOAL & OBJECTIVE

**Final Goal:** Build a website (React + Vite + Tailwind CSS) automatically using AI agents working together.

**User Input:** A description of what website they want (e.g., "Create a SaaS landing page with hero section, features, pricing, and testimonials")

**System Output:** Complete, validated React + Vite + Tailwind CSS code that renders a beautiful website

---

## 🧠 Understanding the Multi-Agent Architecture

### Current State (Research Assistant)
- **One Main Agent** that does everything
- **2 Sub-agents:** Research + Critique
- **1 Tool:** Internet Search

### New State (Website Builder)
- **One Main Orchestrator Agent** (coordinator, not a coder)
- **Multiple Specialized Sub-agents** (each with specific role)
- **Shared Memory System** (file-based state management)
- **Validation Loop** (critique agents)

---

## 🔄 The Agent Flow

```
User Input: "Create a landing page with hero, features, pricing"
                              ↓
                    ┌─────────────────────┐
                    │  Main Orchestrator  │ (coordinates all agents)
                    └─────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
   ┌─────────┐          ┌──────────┐         ┌──────────────┐
   │ Planner │          │ Component│         │ Design       │
   │ Agent   │────────→ │ Search   │────────→ │ Architect    │
   │ (NO     │          │ Agent    │         │ Agent        │
   │ TOOLS)  │          │ (HAS DB  │         │ (NO TOOLS)   │
   └─────────┘          │ TOOL)    │         └──────────────┘
        ↓               └──────────┘                ↓
   Returns:                ↓                   Returns:
   - 5 Component      Returns:             - Theme/Design
     Names           - Top 5 components    - Colors/Sizes
   - Structure         per component       - Layout specs
                      - JSON format       - Content placement
                              ↓
                      ┌──────────────────────┐
                      │  Component Generation│
                      │  Agent               │
                      │  (HAS CODE TOOLS)    │
                      └──────────────────────┘
                              ↓
                         Generate React
                         Components One-by-One
                              ↓
                      ┌──────────────────────┐
                      │ Validation Agents    │
                      │ - Code Critic        │
                      │ - Visual Validator   │
                      └──────────────────────┘
                              ↓
                        Store in DB +
                        Render to Frontend
```

---

## 📋 Agent Breakdown (What We're Building)

### 1️⃣ **Planner Agent** (Sub-agent)
**Purpose:** Break down user request into structured components

**Input:** User description
```
"Create a SaaS landing page with hero section, features, pricing, and testimonials"
```

**Process:**
- Understand user requirements
- Identify needed sections/components
- Create a plan

**Output:** Structure in memory file
```json
{
  "sections": [
    {
      "name": "hero",
      "description": "Eye-catching hero section with CTA"
    },
    {
      "name": "features",
      "description": "Feature list showing key benefits"
    },
    {
      "name": "pricing",
      "description": "Pricing table with 3 plans"
    },
    {
      "name": "testimonials",
      "description": "Social proof with user testimonials"
    }
  ]
}
```

**Tools:** NONE (it's a planning agent)

---

### 2️⃣ **Component Search Agent** (Sub-agent)
**Purpose:** Find existing component designs from database

**Input:** Section/Component name from Planner
```
- "hero section with CTA"
- "feature cards"
- "pricing table"
- "testimonial carousel"
```

**Tool:** 
```python
retrieve_components(component_type: str, count: int = 5) → List[ComponentData]
# Connects to DB/vector database to find similar components
```

**Process:**
- For EACH section from Planner (e.g., 4 sections)
- Search for TOP 5 similar components in database
- Total: 4 sections × 5 components = 20 component options

**Output:** Add to memory file
```json
{
  "sections": [
    {
      "name": "hero",
      "description": "...",
      "candidate_components": [
        { "id": "hero_1", "preview": "...", "design": "..." },
        { "id": "hero_2", "preview": "...", "design": "..." },
        // ... 5 total
      ]
    },
    // ... for each section
  ]
}
```

**Tools:** Database/Vector Search Tool

---

### 3️⃣ **Design Architect Agent** (Sub-agent)
**Purpose:** Select best components and define their styling

**Input:** Candidate components from memory file + User description

**Process:**
- Look at all candidate components
- Pick the BEST one for each section
- Define: colors, sizes, spacing, typography
- Define: how sections connect together
- Create a cohesive design theme

**Output:** Add to memory file
```json
{
  "sections": [
    {
      "name": "hero",
      "selected_component": "hero_1",
      "design_spec": {
        "background_color": "#0f172a",
        "text_color": "#ffffff",
        "button_color": "#3b82f6",
        "layout": "centered",
        "padding": "lg",
        "content": {
          "headline": "Build websites with AI",
          "subheadline": "Create beautiful sites instantly",
          "cta_text": "Get Started"
        }
      }
    }
  ],
  "global_theme": {
    "primary_color": "#3b82f6",
    "secondary_color": "#8b5cf6",
    "font_family": "Inter",
    "spacing_system": "4px base"
  }
}
```

**Tools:** NONE (uses information from search results)

---

### 4️⃣ **Component Generation Agent** (Sub-agent)
**Purpose:** Generate actual React code for components

**Input:** Design specs from memory file

**Process:**
- For EACH section in design_spec
- Generate React component code
- Use Tailwind CSS for styling
- ONE component at a time (not all at once)
- Store result back to memory

**Output:** React components
```jsx
// hero.jsx
export default function Hero() {
  return (
    <div className="bg-slate-900 text-white text-center py-20">
      <h1 className="text-5xl font-bold mb-4">Build websites with AI</h1>
      <p className="text-xl mb-8">Create beautiful sites instantly</p>
      <button className="bg-blue-500 px-8 py-3 rounded">Get Started</button>
    </div>
  )
}
```

**Tools:** Code generation tools (LLM-based)

---

### 5️⃣ **Code Critic Agent** (Sub-agent)
**Purpose:** Validate generated code quality

**Input:** Generated React component code

**Process:**
- Check syntax correctness
- Check React best practices
- Check Tailwind CSS usage
- Check accessibility
- Provide feedback if issues found

**Output:** 
```json
{
  "status": "approved" | "needs_revision",
  "feedback": [
    "Missing alt text on images",
    "Button should have aria-label"
  ]
}
```

**Tools:** Code analysis tools

---

### 6️⃣ **Visual Validator Agent** (Sub-agent)
**Purpose:** Validate visual appearance against design specs

**Input:** 
- Generated React code
- Design specification
- (Eventually) Screenshot/rendered output

**Process:**
- Compare generated code against design specs
- Check if colors match
- Check if layout matches
- Check if spacing matches
- Provide visual feedback

**Output:**
```json
{
  "status": "matches_design" | "needs_revision",
  "issues": [
    "Color mismatch on button",
    "Spacing too tight"
  ]
}
```

**Tools:** Visual comparison tools

---

## 💾 Memory System (Shared State)

### What is Memory?
A **single source of truth** that all agents read from and write to.

### Current Plan: File-based (Virtual Memory)
NOT a database, but a JSON file that serves as:
- **State container**: Current progress
- **Communication channel**: Agents pass data to each other
- **Audit trail**: What happened at each step

### Memory Structure
```json
{
  "user_input": "Create a SaaS landing page...",
  "status": "in_progress",
  "timestamp": "2025-11-16T10:30:00Z",
  
  "planning_phase": {
    "status": "complete",
    "sections": [...],
    "timestamp": "2025-11-16T10:31:00Z"
  },
  
  "component_search_phase": {
    "status": "complete",
    "sections_with_candidates": [...],
    "timestamp": "2025-11-16T10:35:00Z"
  },
  
  "design_phase": {
    "status": "complete",
    "design_specs": [...],
    "global_theme": {...},
    "timestamp": "2025-11-16T10:40:00Z"
  },
  
  "generation_phase": {
    "status": "in_progress",
    "components_generated": {
      "hero": {
        "code": "...",
        "status": "generated",
        "validation": {
          "code_critic": {...},
          "visual_validator": {...}
        }
      }
    },
    "timestamp": "2025-11-16T10:45:00Z"
  }
}
```

### Is it Virtual?
**Yes** - It exists only during the agent execution session:
- Loaded when needed
- Updated by agents
- Passed between agents
- Discarded after final code is generated

---

## 🎯 Current Implementation Strategy

### STEP 1: Modify Current Prompt (THIS IS FIRST!)
**What:** Change the main orchestrator to not use subagents initially

**Why:** We need to understand how the new workflow should work first

**Action:**
- Keep the same `main agent` structure
- Remove research/critique sub-agents
- Create a new prompt that explains the website builder workflow
- Test it to understand agent behavior

### STEP 2: Implement Agents One-by-One
1. Planner Agent
2. Component Search Agent (with DB tool)
3. Design Architect Agent
4. Component Generation Agent
5. Code Critic Agent
6. Visual Validator Agent

### STEP 3: Create Memory System
- In-memory JSON structure
- Agent read/write functions
- Memory update protocols

### STEP 4: Connect Agents
- Main orchestrator coordinates flow
- Each agent reads/writes from memory
- Pass control between agents

---

## ❓ Key Questions to Answer

### 1. **Memory Implementation**
- Virtual (in-memory JSON) vs File-based (.json file)?
- **Decision:** Start with virtual (in-memory), upgrade to file-based later if needed

### 2. **Component Database**
- Where do we get component designs?
- How do we store them?
- **Decision:** Will implement mock database first, then real one

### 3. **Code Output**
- Single file or multiple files?
- How to structure the React project?
- **Decision:** Generate as modular components, export as structured project

### 4. **Validation Loop**
- When does visual validation happen?
- How many iterations?
- **Decision:** Validate each component, fix if needed, move to next

---

## 📊 Implementation Roadmap

```
PHASE 1: Update Main Prompt
  ├─ Remove research/critique sub-agents
  ├─ Create website builder workflow prompt
  └─ Test with simple example

PHASE 2: Create Planner Agent
  ├─ Implement planner sub-agent
  ├─ Create memory structure
  └─ Test planning output

PHASE 3: Create Component Search Agent
  ├─ Implement search sub-agent
  ├─ Create mock component database
  ├─ Implement search tool
  └─ Test component retrieval

PHASE 4: Create Design Architect Agent
  ├─ Implement design agent
  ├─ Create design specification format
  └─ Test design output

PHASE 5: Create Component Generation Agent
  ├─ Implement generation agent
  ├─ Create React code generation
  └─ Test component output

PHASE 6: Create Validation Agents
  ├─ Implement code critic
  ├─ Implement visual validator
  └─ Test validation loop

PHASE 7: Integration & Testing
  ├─ Connect all agents
  ├─ Test full workflow
  └─ Refine and optimize
```

---

## 🚀 Next Actions

1. **Confirm Understanding**: Do you agree with this structure?
2. **Start PHASE 1**: Update the current prompt to workflow-based
3. **Keep it Simple**: Don't implement sub-agents yet, just understand the flow

---

## 📝 Questions Before We Start

1. **Memory**: Virtual (in-memory) or File-based?
2. **Component DB**: Mock or Real?
3. **Scope**: Start with simple components or full pages?
4. **Output Format**: Single file or project structure?

Let me know your thoughts and we'll proceed with PHASE 1! 🎯
