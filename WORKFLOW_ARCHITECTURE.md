# 🔄 UPDATED WORKFLOW ARCHITECTURE - File-Based Memory

## Overview

The multi-agent system now uses a **file-based memory pattern** where each agent:
1. **Reads** output from previous agent
2. **Processes** the work
3. **Writes** to its own output file
4. **Next agent** reads that file and continues

This keeps context focused and low-token while maintaining clear workflow.

---

## Workflow Chain

```
USER INPUT
    ↓
PHASE 1: PLANNER AGENT
    ├─ INPUT: User's website requirement
    ├─ PROCESS: Breaks down requirements
    └─ OUTPUT FILE: website_plan.md
        ↓
PHASE 2: COMPONENT SEARCH AGENT
    ├─ INPUT FILE: website_plan.md
    ├─ PROCESS: Searches components using RAG tool
    └─ OUTPUT FILE: component_references.md
        ↓
PHASE 3: DESIGN ARCHITECT AGENT (Future)
    ├─ INPUT FILE: component_references.md
    ├─ PROCESS: Creates design specifications
    └─ OUTPUT FILE: design_specs.md
        ↓
PHASE 4: COMPONENT GENERATOR AGENT (Future)
    ├─ INPUT FILE: design_specs.md
    ├─ PROCESS: Generates React component code
    └─ OUTPUT FILE: generated_code.md
        ↓
PHASE 5: CODE CRITIC AGENT (Future)
    ├─ INPUT FILE: generated_code.md
    ├─ PROCESS: Reviews code quality
    └─ OUTPUT FILE: code_review.md
        ↓
PHASE 6: VISUAL VALIDATOR AGENT (Future)
    ├─ INPUT FILE: code_review.md
    ├─ PROCESS: Validates design and accessibility
    └─ OUTPUT FILE: validation_report.md
        ↓
FINAL OUTPUT: All files + summary
```

---

## File Structure (Memory)

```
website_project/
├── website_plan.md              ← Planner output
├── component_references.md      ← Component Search output
├── design_specs.md              ← Design Architect output (Phase 4)
├── generated_code.md            ← Generator output (Phase 5)
├── code_review.md               ← Critic output (Phase 6)
├── validation_report.md         ← Validator output (Phase 7)
└── src/                         ← Final React project (generated from code)
    ├── components/
    ├── pages/
    └── ...
```

---

## Current Implementation Status

### ✅ PHASE 1: PLANNER AGENT
- **Status**: Implemented
- **Input**: User website requirement
- **Output File**: `website_plan.md`
- **Sub-agent**: `planner_agent`
- **Tools**: None (prompt-based)

### ✅ PHASE 2: COMPONENT SEARCH AGENT
- **Status**: UPDATED with file-based flow
- **Input File**: `website_plan.md` (created by planner)
- **Output File**: `component_references.md`
- **Sub-agent**: `component_search_agent`
- **Tools**: `component-search` (RAG-based)
- **Process**:
  1. Read `website_plan.md`
  2. Extract component inventory
  3. For each component: Call component-search tool
  4. Get results with code, colors, fonts
  5. Write to `component_references.md`

### 🔜 PHASE 3: DESIGN ARCHITECT AGENT
- **Status**: To implement (Phase 4)
- **Input File**: `component_references.md`
- **Output File**: `design_specs.md`
- **Tools**: Possibly design utilities

### 🔜 PHASE 4: COMPONENT GENERATOR
- **Status**: To implement (Phase 5)
- **Input File**: `design_specs.md`
- **Output File**: `generated_code.md`
- **Tools**: Code generation tools

### 🔜 PHASE 5: CODE CRITIC
- **Status**: To implement (Phase 6)
- **Input File**: `generated_code.md`
- **Output File**: `code_review.md`
- **Tools**: Linting, analysis tools

### 🔜 PHASE 6: VISUAL VALIDATOR
- **Status**: To implement (Phase 7)
- **Input File**: `code_review.md`
- **Output File**: `validation_report.md`
- **Tools**: Accessibility, design validation tools

---

## Orchestrator Instructions (Updated)

The main orchestrator tells each agent:

```python
PHASE 1:
  "Use planner-agent to analyze requirements and write to website_plan.md"

PHASE 2:
  "Use component-search-agent to:
   - Read website_plan.md
   - Search components for each item
   - Write findings to component_references.md"

PHASE 3:
  "Use design-architect-agent to:
   - Read component_references.md
   - Create design specifications
   - Write to design_specs.md"

... and so on
```

---

## Benefits of File-Based Architecture

✅ **Low Context**: Each agent only reads what it needs  
✅ **Clear Handoff**: File names explicit in prompts  
✅ **Traceability**: See each phase's output  
✅ **Reusability**: Can re-run phases independently  
✅ **Debugging**: Easy to check what each agent did  
✅ **Scalability**: Easy to add new phases  
✅ **Parallel Processing**: Multiple agents could run in parallel  
✅ **Version Control**: Git tracks changes per phase  

---

## Implementation Checklist

### Phase 1 (Planner)
- [x] Implemented
- [x] Outputs to `website_plan.md`

### Phase 2 (Component Search)
- [x] Agent defined
- [x] Tool with RAG created
- [x] Updated to read `website_plan.md`
- [x] Updated to write `component_references.md`
- [x] Added file names to agent prompt
- [ ] Test implementation

### Phase 3+ (Future)
- [ ] Design Architect Agent
- [ ] Component Generator Agent
- [ ] Code Critic Agent
- [ ] Visual Validator Agent

---

## Example: Phase 2 Flow

```
1. Main Orchestrator:
   "Use component-search-agent to find components"

2. Component Search Agent reads:
   website_plan.md (has component inventory)
   
3. For each component:
   - Extract: type, specification, features
   - Call: component-search tool
   - Get: code, colors, fonts, tailwind classes
   
4. Agent writes to:
   component_references.md
   
5. Next agent (Phase 3) reads:
   component_references.md
   (and uses it for design specifications)
```

---

## File Format Example

### website_plan.md (Planner Output)
```markdown
# Website Plan

## Project Overview
- Type: SaaS Landing Page
- Purpose: Showcase DataFlow analytics platform
- Target: Small business owners

## Component Inventory
1. Navigation Bar
   - Type: navigation
   - Features: logo, menu, responsive
   
2. Hero Banner
   - Type: hero
   - Features: headline, subtext, CTA button
   
3. Feature Cards
   - Type: card
   - Features: icon, title, description
   
...
```

### component_references.md (Component Search Output)
```markdown
# Component Reference Guide

## Design System
- Primary Color: #1e3a8a (Dark Blue)
- Font: Inter, sans-serif

## Components Found

### 1. Navigation Bar
- Match Score: 0.94
- Code:
  ```jsx
  [Full component code]
  ```
- Colors: #1e3a8a, #0ea5e9
- Font: Inter

### 2. Hero Banner
- Match Score: 0.91
- Code:
  ```jsx
  [Full component code]
  ```
- Colors: #1e3a8a, #ffffff
- Font: Inter

...
```

### design_specs.md (Design Architect Output - Future)
```markdown
# Design Specifications

## Color Palette
- Primary: #1e3a8a
- Secondary: #0ea5e9
- Accent: #ff6b35

## Typography
- Headings: Inter Bold
- Body: Inter Regular

## Component Specifications
### Navigation
- Size: 60px height
- Background: White with shadow
- Text: Dark blue

...
```

---

## Key Points for Implementation

1. **File Names Matter**: Agents must know exact file names to read/write
2. **Agent Prompts**: Update prompts to include:
   - INPUT FILE: `[filename]`
   - OUTPUT FILE: `[filename]`
3. **Sequential Flow**: Each phase depends on previous
4. **Clean Separation**: One phase = one file output
5. **Explicit Instructions**: Tell agents what to read and write

---

## Next Steps

1. ✅ Update Phase 2 documentation (DONE)
2. ✅ Update Phase 3 guide (DONE)
3. ⬜ Test Phase 2 implementation
4. ⬜ Implement Phase 3 code
5. ⬜ Test Phase 2-3 integration
6. ⬜ Create Phase 4 guide
7. ⬜ Continue with remaining phases

---

**Architecture Updated** ✅ | Ready for implementation! 🚀
