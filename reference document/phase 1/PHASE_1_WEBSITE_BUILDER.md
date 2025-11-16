# 🎯 PHASE 1: Update Main Prompt - Implementation Guide

## Objective
Change the current research agent prompt to a **website builder orchestrator prompt** without implementing sub-agents yet.

This is just to understand the workflow and see how the agent behaves.

---

## Current State
```
Main Agent (Research)
  ├─ Tool: Internet Search
  ├─ Sub-agent: Research
  └─ Sub-agent: Critique
```

## New State (For Understanding)
```
Main Agent (Website Builder Orchestrator)
  ├─ No tools yet
  ├─ No sub-agents yet
  └─ Just prompt-based workflow
```

---

## What We'll Change

### File to Modify
`src/services/agent_service.py`

### Current Prompt (Research)
```python
research_instructions = """You are an expert researcher...
Use the research-agent to conduct deep research...
When you think you have enough information, write the final report...
"""
```

### New Prompt (Website Builder)
```python
website_builder_instructions = """You are an AI Website Builder Orchestrator.

Your job is to guide the website creation process step-by-step.

WORKFLOW:
1. PLANNING PHASE: Understand what website the user wants
   - Ask: What type of website? (landing page, portfolio, SaaS, etc.)
   - Ask: What sections needed? (hero, features, pricing, etc.)
   - Identify the structure

2. COMPONENT SELECTION PHASE: (will be component search agent later)
   - For each section, list candidate components
   - Store in memory file

3. DESIGN PHASE: (will be design architect agent later)
   - Choose best components
   - Define colors, fonts, spacing
   - Create design specification

4. GENERATION PHASE: (will be component generation agent later)
   - Generate React code for each section
   - Use Tailwind CSS for styling
   - Output Vite + React structure

5. VALIDATION PHASE: (will be critic agents later)
   - Validate code quality
   - Check visual appearance
   - Fix any issues

CURRENT LIMITATION: You will do all these steps as ONE AGENT.
Later, we will break this down into specialized sub-agents.

Start by understanding the user's website requirements.
"""
```

---

## Implementation Steps

### Step 1: Open the file
```
src/services/agent_service.py
```

### Step 2: Find the `research_instructions` variable
This is the system prompt for the agent.

### Step 3: Replace it with new prompt
Keep the same structure but change:
- Agent role: From "researcher" to "website builder"
- Tasks: From "research" to "website building"
- Output: From "reports" to "React code"

### Step 4: Keep everything else the same
- Don't change agent creation
- Don't change tools
- Don't change middleware
- Don't add sub-agents yet

### Step 5: Test it
```bash
python luna.py prompt "Create a SaaS landing page with hero, features, and pricing"
```

---

## Expected Behavior

The agent should:
1. Acknowledge it's a website builder
2. Ask about your website requirements (or infer them)
3. Create a plan
4. Describe what components would be needed
5. Outline the design approach
6. Try to generate React code

**Note:** It might not be perfect yet - that's okay! 
We're just understanding the workflow.

---

## Success Criteria

- ✅ Agent responds to website building prompts
- ✅ Agent mentions planning steps
- ✅ Agent talks about components
- ✅ Agent discusses React/Tailwind
- ✅ No errors or crashes
- ✅ Prompt is clear and understandable

---

## What NOT to Do

❌ Don't add sub-agents yet
❌ Don't add tools yet
❌ Don't implement memory file
❌ Don't generate actual code yet

---

## After PHASE 1

Once we confirm this works:
- PHASE 2: Create Planner sub-agent
- PHASE 3: Create Component Search sub-agent
- And so on...

---

## Timeline
- PHASE 1: 1-2 hours (just update prompt)
- Testing: 30 minutes
- Feedback: Based on results

Ready to proceed? 🚀
