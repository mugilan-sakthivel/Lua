# 🎯 PHASE 2: Create Planner Agent - Implementation Guide

## Objective

Implement the **Planner Sub-Agent** that breaks down website requirements into a structured plan.

**What it does:**

- Takes user's website requirements as input
- Analyzes and understands what the user wants
- Creates a detailed project plan with:
  - Website type and purpose
  - Page structure and layout
  - Key features and sections
  - Component list needed
  - Design approach
- **Writes** plan to `website_plan.md` for other agents to read

---

## Current Architecture

```
Main Agent (Website Builder Orchestrator)
  ├─ Tool: Internet Search
  ├─ Sub-agent: Critique (existing)
  ├─ Sub-agent: Research (existing)
  └─ Sub-agent: Planner (TO CREATE) ⭐
```

---

## Phase 2 Tasks

### Task 1: Create Planner Sub-Agent File

**File to create:** `src/subagents/planner_agent.py`

**Purpose:** Define the planner sub-agent with its own system prompt

**Structure:**

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent

# Planner agent system prompt
planner_instructions = """
You are a Website Planning Expert. Your role is to analyze user requirements
and create a detailed project plan for website creation.

## YOUR RESPONSIBILITIES:
1. Understand what website the user wants to build
2. Identify the purpose and target audience
3. Break down requirements into features and pages
4. Create a site structure and information architecture
5. List all components needed
6. Plan responsive design approach
7. Document design principles and constraints

## ANALYSIS FRAMEWORK:

When given website requirements, analyze:

1. **WEBSITE TYPE**: What kind of website?
   - Landing page
   - Portfolio
   - SaaS product
   - E-commerce
   - Blog
   - Corporate
   - Other

2. **PURPOSE & GOALS**:
   - Primary goal (sell, inform, showcase)
   - Target audience
   - Key conversions/actions

3. **REQUIRED PAGES**:
   - Home page
   - About page
   - Services/Features page
   - Pricing page
   - Contact page
   - Blog/Resources
   - Other pages

4. **KEY SECTIONS** (for each page):
   - Header/Navigation
   - Hero section
   - Features
   - Testimonials
   - Pricing
   - Call-to-action
   - Footer
   - Other sections

5. **COMPONENTS NEEDED**:
   - Navigation component
   - Hero banner
   - Feature cards
   - Pricing cards
   - Testimonial cards
   - Forms
   - Buttons
   - Icons
   - Images
   - Other components

6. **DESIGN REQUIREMENTS**:
   - Color scheme preferences
   - Font/typography style
   - Brand guidelines (if any)
   - Animation preferences
   - Responsive breakpoints needed

7. **CONSTRAINTS & NOTES**:
   - Performance requirements
   - Accessibility needs
   - Browser support
   - Mobile-first or desktop-first
   - Any special features

## OUTPUT FORMAT:

Create a detailed plan document with clear sections:

## Website Plan

### Project Overview
- **Website Type**: [Type]
- **Purpose**: [Main goal]
- **Target Audience**: [Who it's for]
- **Key Success Metrics**: [What defines success]

### Site Structure
```

[Page hierarchy/sitemap]

```

### Page Details
For each page:
- **Page Name**: [Name]
- **Purpose**: [What this page does]
- **Key Sections**: [List sections]
- **Components**: [Components needed on this page]

### Component Inventory
Complete list of all unique components needed with:
- Component name
- Purpose
- Key features
- Interaction requirements

### Design Approach
- **Color Scheme**: [Colors and their usage]
- **Typography**: [Font choices and sizing]
- **Layout**: [Grid, spacing, responsive breakpoints]
- **Animation**: [Movement and transitions]
- **Responsive Design**: [Mobile, tablet, desktop considerations]

### Implementation Notes
- Any special requirements
- Performance considerations
- Accessibility notes
- Browser support needs

## GUIDELINES:
- Be thorough and specific
- Ask for clarification if requirements are vague
- Think about user experience
- Consider mobile-first approach
- Plan for scalability and maintainability
- Document everything clearly

Your output becomes the blueprint for other agents to follow.
"""

def create_planner_agent():
    """Create and return the planner sub-agent.

    Returns:
        A LangChain agent for website planning
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    agent = create_deep_agent(
        model=model,
        tools=[],  # Planner doesn't need external tools yet
        system_prompt=planner_instructions,
        subagents=[],  # No sub-agents for planner
    )

    return agent


# Export for use in main agent
planner_agent = create_planner_agent()
```

---

### Task 2: Import Planner Agent in Main Service

**File to update:** `src/services/agent_service.py`

**Changes:**

1. Add import at the top:

```python
from src.subagents import research_sub_agent, critique_sub_agent, planner_agent
```

2. Add planner to subagents list in `create_website_builder_agent()`:

```python
agent = create_deep_agent(
    model=model,
    tools=[internet_search],
    system_prompt=website_builder_instructions,
    subagents=[critique_sub_agent, research_sub_agent, planner_agent],  # Added planner
)
```

---

### Task 3: Update Main Orchestrator Prompt

**File to update:** `src/services/agent_service.py`

**Update the `website_builder_instructions` to explicitly call the planner:**

```python
## WORKFLOW ORCHESTRATION:

When a user provides website requirements:

1. **PLANNING PHASE**: Use the planner-agent to:
   - Understand the website requirements
   - Analyze the user's needs
   - Create a detailed project plan
   - Output: A detailed project plan (save to `website_plan.md`)

   INSTRUCTION TO AGENT: "Please use the planner-agent to create a detailed plan"
```

---

### Task 4: Update Subagents **init**.py

**File to update:** `src/subagents/__init__.py`

**Changes:**

```python
"""Sub-agents for Luna website builder."""

from .research_agent import research_sub_agent
from .critique_agent import critique_sub_agent
from .planner_agent import planner_agent

__all__ = ["research_sub_agent", "critique_sub_agent", "planner_agent"]
```

---

### Task 5: Create Test Script for Planner

**File to create:** `test_planner_agent.py`

**Purpose:** Test the planner agent independently

```python
#!/usr/bin/env python3
"""Test script for the planner agent."""

from src.subagents import planner_agent

def test_planner():
    """Test the planner agent with a sample website requirement."""

    print("\n" + "=" * 70)
    print("          📋 Planner Agent - Test")
    print("=" * 70)

    sample_requirement = """
    I need a landing page for my SaaS product called "DataFlow".

    It's a data analytics platform that helps small businesses understand their data.

    I want:
    - Clean, modern design
    - Hero section with clear value proposition
    - 3-4 features showcased
    - Pricing section (3 tiers)
    - Customer testimonials
    - Call-to-action buttons throughout
    - Mobile responsive

    The color scheme should be professional - blues and whites with a touch of orange accent.
    Font should be modern sans-serif like Inter.
    """

    print(f"\n📝 Requirement:\n{sample_requirement}\n")
    print("🔄 Planner Agent: Processing...\n")
    print("-" * 70)

    try:
        response = planner_agent.invoke({"input": sample_requirement})

        print("\n" + "-" * 70)
        print("\n📋 Plan Output:\n")
        print(response)
        print("\n" + "=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_planner()
```

---

## Implementation Checklist

- [ ] Create `src/subagents/planner_agent.py`
- [ ] Define `planner_instructions` prompt
- [ ] Implement `create_planner_agent()` function
- [ ] Update `src/subagents/__init__.py` to export planner_agent
- [ ] Update `src/services/agent_service.py` to import planner_agent
- [ ] Add planner_agent to subagents list in main orchestrator
- [ ] Update main prompt to reference planner-agent explicitly
- [ ] Create `test_planner_agent.py` test script
- [ ] Test planner agent with sample website requirement
- [ ] Verify plan output format and quality
- [ ] Document planner agent usage

---

## Expected Outputs

When you run the test with a SaaS landing page requirement, the planner should output:

```markdown
## Website Plan

### Project Overview

- **Website Type**: SaaS Landing Page
- **Purpose**: Showcase DataFlow analytics platform and drive signups
- **Target Audience**: Small business owners and decision-makers
- **Key Success Metrics**: Email signups, demo requests, product understanding

### Site Structure
```

Home Page
├── Header (Navigation + Logo)
├── Hero Section
├── Features Section
├── How It Works Section
├── Pricing Section
├── Testimonials Section
├── CTA Section
├── Footer

```

### Component Inventory
1. **Navigation** - Header with logo and nav links
2. **Hero Banner** - Large headline, subtext, CTA button
3. **Feature Card** - Icon, title, description
4. **Pricing Card** - Plan name, price, features list, CTA button
5. **Testimonial Card** - Author photo, quote, name/title
6. **CTA Button** - Various sizes and states
7. **Icon Set** - Feature icons
8. **Form** - Email signup form
9. **Footer** - Links, social media, copyright

### Design Approach
- **Color Scheme**:
  - Primary: Blue (#1e3a8a)
  - Secondary: Orange (#ff6b35)
  - Background: White/Light gray
- **Typography**: Inter sans-serif
- **Layout**: Mobile-first, responsive grid
- **Animation**: Subtle fade-ins and hover effects
- **Responsive**: Mobile (320px), Tablet (768px), Desktop (1024px)

...
```

---

## Success Criteria

✅ Planner agent successfully created  
✅ Planner prompt is comprehensive and clear  
✅ Agent can be imported and used by main orchestrator  
✅ Test script runs without errors  
✅ Plan output is detailed and actionable  
✅ Format is consistent and well-organized

---

## Next Phase (Phase 3)

After Phase 2 is complete and working:

- Create Component Search Agent
- Implement mock component database
- Create component search/retrieval tool
- Test component discovery

---

## 📚 Related Files

- `src/services/agent_service.py` - Main orchestrator
- `src/subagents/__init__.py` - Sub-agent exports
- `src/subagents/planner_agent.py` - TO CREATE
- `test_planner_agent.py` - TO CREATE

---

**Phase 2 Guide Complete** ✅ | Ready to implement! 🚀
