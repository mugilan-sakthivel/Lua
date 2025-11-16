# Phase 4: Design Architect Agent Implementation

## Overview

Phase 4 implements the **Design Architect Agent** - a specialized sub-agent that takes the planning output and component references, then creates comprehensive visual design specifications including color schemes, typography, layout, spacing, and responsive design details.

## Architecture

### System Flow

```
Phase 3 Outputs (website_plan.md + component_references.md)
            ↓
Design Architect Agent
    ├── Reads website_plan.md
    ├── Reads component_references.md
    ├── Analyzes design requirements
    ├── Selects best components for each section
    ├── Defines color scheme
    ├── Defines typography system
    ├── Creates layout specifications
    └── Writes design_specs.md
            ↓
Phase 5: Component Generator Agent
    └── Reads design_specs.md
```

## What Design Architect Does

### Inputs

1. **website_plan.md** - Architecture, pages, sections, components needed
2. **component_references.md** - Available components with code and styling

### Processing Steps

1. **Component Selection** - For each section, picks the best matching component
2. **Design System Definition** - Creates unified color, typography, spacing rules
3. **Layout Specification** - Defines grid, responsive breakpoints, spacing
4. **Visual Consistency** - Ensures all components work together harmoniously
5. **Responsive Design Plan** - Mobile, tablet, desktop specifications

### Output

**design_specs.md** - Complete design specifications ready for code generation

## Implementation Tasks

### Task 1: Create Design Architect Sub-Agent

**File**: `src/subagents/design_architect_agent.py`

Create a new sub-agent with the following responsibilities:

````python
sub_design_architect_prompt = """You are a Professional UI/UX Design Architect specializing in creating cohesive design systems for React websites.

## YOUR RESPONSIBILITIES:

1. Read the website plan from `website_plan.md`
2. Read the component references from `component_references.md`
3. Create a comprehensive design specification document
4. Ensure visual consistency across all components
5. Define the complete design system

## PROCESS:

### Step 1: Analyze Requirements
- Extract page structure from website_plan.md
- Identify all required components
- Note any design preferences or constraints

### Step 2: Component Selection
For each page section:
- Review available components from component_references.md
- Select the best matching component
- Note why this component was chosen
- Document any modifications needed

### Step 3: Design System Definition

#### Color Palette:
- Primary Color: [Hex code from components]
- Secondary Color: [Hex code from components]
- Accent Color: [Optional]
- Neutral Colors: [Grays for text, backgrounds]
- Status Colors: [Success, warning, error, info]

#### Typography:
- Font Family: [From components]
- Heading Styles: h1-h6 with sizes, weights, line-heights
- Body Text: Size, weight, line-height
- Small Text: For captions, labels, meta information

#### Spacing System:
- Base Unit: 4px, 8px, or 16px
- Scale: [xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px, ...]
- Padding rules for components
- Margin rules for layouts

#### Layout:
- Grid System: [12-col, 16-col, etc.]
- Responsive Breakpoints:
  - Mobile: 320px - 480px
  - Tablet: 481px - 768px
  - Desktop: 769px - 1024px
  - Wide: 1025px+
- Container widths for each breakpoint

### Step 4: Create Design Specifications
Document for each page/section:
- Page name
- Purpose
- Layout type (hero, feature grid, etc.)
- Components used (with names from component_references.md)
- Color scheme specific to this page
- Typography hierarchy
- Responsive behavior

### Step 5: Visual Consistency Rules
- Ensure color usage is consistent
- Verify typography follows hierarchy
- Check spacing is uniform
- Validate component interactions

## OUTPUT FORMAT:

Create `design_specs.md` with structure:

```markdown
# Design Specification Document

## Design System

### Color Palette
- Primary: [Color] ([Hex])
- Secondary: [Color] ([Hex])
- ...

### Typography
- Font Family: [Font]
- Sizes & Weights: [Specifications]

### Spacing System
- Base Unit: [Value]
- Scale: [Scale values]

### Layout Grid
- Grid Type: [Type]
- Columns: [Number]
- Breakpoints: [Specifications]

## Pages & Sections

### [Page Name]
- **Purpose**: [What this page does]
- **Sections**: [List of sections]

#### [Section Name]
- **Component**: [Component name from references]
- **Layout**: [How it's arranged]
- **Colors**: [Specific colors used]
- **Typography**: [Heading/text sizes]
- **Spacing**: [Padding/margin specs]
- **Responsive Behavior**: [How it adapts]

## Component Usage Guide

### [Component Name]
- **Used In**: [Pages where it appears]
- **Color Scheme**: [Colors applied]
- **Sizing**: [Dimensions]
- **States**: [Hover, active, disabled]

## Design System Rules

### Color Usage
- Primary: [When to use]
- Secondary: [When to use]
- ...

### Typography Hierarchy
- Headings: [h1-h6 sizes and weights]
- Body: [Text sizing]
- Labels: [For forms and components]

### Responsive Design Notes
- Mobile considerations: [Specific notes]
- Tablet considerations: [Specific notes]
- Desktop considerations: [Specific notes]
````

## GUIDELINES:

- Be thorough in design specifications
- Ensure visual harmony
- Consider accessibility (color contrast, readability)
- Plan for responsive design
- Maintain consistency across all pages
- Document design decisions
- Consider performance implications

Your output becomes the blueprint for code generation in Phase 5.
"""

design_architect_agent = {
"name": "design-architect-agent",
"description": "Creates comprehensive design specifications from plan and components. Reads website_plan.md and component_references.md, writes design_specs.md with colors, typography, layout, and responsive design details.",
"system_prompt": sub_design_architect_prompt,
}

````

### Task 2: Update Subagents Exports

**File**: `src/subagents/__init__.py`

Add design architect to exports:

```python
from .design_architect_agent import design_architect_agent

__all__ = [
    "research_sub_agent",
    "planner_agent",
    "critique_sub_agent",
    "component_search_agent",
    "design_architect_agent",  # Add this
]
````

### Task 3: Update Agent Service

**File**: `src/services/agent_service.py`

1. Import the design architect agent:

```python
from src.subagents import (
    research_sub_agent,
    planner_agent,
    component_search_agent,
    design_architect_agent,  # Add this
)
```

2. Update the workflow prompt to include Phase 4:

```python
### Sub-Agents You Have:
1. **planner_agent** - Creates website plan (website_plan.md)
2. **component_search_agent** - Finds components (component_references.md)
3. **design_architect_agent** - Creates design specs (design_specs.md)  # Add this
```

3. Add design architect to the subagents list:

```python
agent = create_deep_agent(
    model=model,
    tools=[internet_search, component_search_tool],
    system_prompt=website_builder_instructions,
    subagents=[
        planner_agent,
        component_search_agent,
        design_architect_agent,  # Add this
    ],
)
```

## Design Architect Workflow

### Input Files Required

- `website_plan.md` - From planner agent (Phase 2)
- `component_references.md` - From component search agent (Phase 3)

### Processing Flow

1. **Read Plans** - Load both input files
2. **Analyze Structure** - Understand page hierarchy and sections
3. **Review Components** - Check available components and their properties
4. **Design Color System** - Select cohesive color palette
5. **Design Typography** - Create font hierarchy
6. **Layout Planning** - Define grid and spacing
7. **Responsive Strategy** - Plan breakpoints and adaptations
8. **Document Everything** - Write comprehensive specifications

### Output File

- `design_specs.md` - Complete design specification ready for code generation

## Key Design Decisions

### Color Scheme Strategy

- Use 3-5 colors max (primary, secondary, accent + neutrals)
- Extract from component references
- Ensure WCAG AA contrast ratios
- Plan for dark mode if needed

### Typography Strategy

- 2-3 font families max (one serif, one sans-serif usually)
- 5-7 font sizes for different purposes
- Consistent line-height ratios (1.5 for body, 1.2 for headings)
- Consider readability and accessibility

### Layout Strategy

- 12-column grid (most common)
- 4-5 responsive breakpoints
- Consistent spacing scale (4px, 8px, 16px multiples)
- Mobile-first approach

### Responsive Strategy

- Mobile: Single column, optimized for touch
- Tablet: 2-column layouts, medium text
- Desktop: Full multi-column layouts

## Design System Documentation

The design architect should create clear documentation for:

1. **Component Usage** - When to use each component
2. **Color Rules** - How to apply colors correctly
3. **Typography Rules** - Font sizing and hierarchy
4. **Spacing Rules** - Padding and margin guidelines
5. **Responsive Rules** - How components adapt

## Phase 4 Deliverables Checklist

- [ ] `src/subagents/design_architect_agent.py` created
- [ ] Agent imports design prompt and sub-agent definition
- [ ] `src/subagents/__init__.py` updated with design_architect_agent export
- [ ] `src/services/agent_service.py` updated with:
  - [ ] Design architect import
  - [ ] Design architect in agent description
  - [ ] Design architect in subagents list
- [ ] `design_specs.md` generated correctly with:
  - [ ] Design system (colors, typography, spacing, layout)
  - [ ] Page specifications
  - [ ] Component usage guide
  - [ ] Design system rules
- [ ] Testing complete - agent can generate design specs
- [ ] Documentation updated

## Testing Phase 4

### Test Input

Create a test website plan and component references, then test:

```python
# Test that design architect generates proper specifications
# Check that design_specs.md has all required sections:
# - Color palette
# - Typography system
# - Layout specifications
# - Page/section details
# - Responsive design notes
```

### Validation Points

- ✅ Colors are cohesive and from components
- ✅ Typography follows hierarchy
- ✅ Spacing is consistent
- ✅ Layout is responsive
- ✅ All sections documented

## Integration with Next Phases

### Phase 5: Component Generator

- Reads `design_specs.md`
- Uses specifications to generate React code
- Applies colors, fonts, spacing defined here

### Phase 6: Code Critic

- Reviews code against design specs
- Ensures implementation matches design

### Phase 7: Visual Validator

- Validates generated code matches specifications

## Timeline

**Estimated**: 3-5 hours

- Design architect agent creation: 1 hour
- Integration with agent service: 1 hour
- Testing and validation: 1-2 hours
- Documentation: 1 hour

## Next Steps

1. Create `src/subagents/design_architect_agent.py`
2. Update subagents `__init__.py`
3. Update `src/services/agent_service.py`
4. Test with sample website requirements
5. Generate `design_specs.md` for verification
6. Document any design patterns discovered

## Resources

- [Design Systems Best Practices](https://www.designsystems.com/)
- [Spacing Systems](https://www.spacingsystem.com/)
- [Typography Scales](https://www.typescale.com/)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Responsive Design Patterns](https://www.smashingmagazine.com/web-design-patterns/)

## Summary

Phase 4 creates the Design Architect Agent that transforms planning and component discovery into a comprehensive design specification document. This specification serves as the blueprint for code generation in Phase 5.

The Design Architect:

- ✅ Selects best components for each section
- ✅ Defines cohesive design system
- ✅ Creates color and typography specifications
- ✅ Plans responsive layouts
- ✅ Documents all design decisions
- ✅ Provides foundation for code generation
