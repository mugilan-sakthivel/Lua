# 🚀 Luna Website Builder - Quick Start with Conversation Persistence

## Installation

```bash
cd /path/to/lunapy_v2
pip install -r requirements.txt
```

---

## Basic Usage

### 1. Interactive Mode (Recommended)

```bash
python luna.py
```

**Features:**
- Natural conversation flow
- Full context maintained automatically
- Special commands: `clear`, `stats`, `exit`

**Example:**
```
🤖 You: Build a portfolio website for a designer
✅ Agent: [creates plan, searches components, generates code]

🤖 You: Add a dark mode toggle
✅ Agent: [remembers it's a portfolio site, adds dark mode]

🤖 You: stats
📊 Total messages: 4, User: 2, Assistant: 2
```

---

### 2. Prompt Mode (Single Commands)

```bash
python luna.py prompt "your requirement here"
```

**Example:**
```bash
# First request
python luna.py prompt "Build an e-commerce website"

# Follow-up (remembers context)
python luna.py prompt "Add product filtering"
```

---

## Conversation Management

### View Statistics
```bash
python luna.py stats
```

### Export Conversation
```bash
python luna.py export conversation_backup.txt
```

### Clear History
```bash
python luna.py clear
```

---

## Multi-Agent Workflow

Luna automatically orchestrates 6 specialized agents:

1. **Planner** → Creates `website_plan.md`
2. **Component Search** → Creates `component_references.md`
3. **Design Architect** → Creates `design_specs.md`
4. **Component Generator** → Creates React components
5. **Code Critic** → Reviews and fixes code
6. **Visual Validator** → Generates preview

**All files are automatically created in the correct locations!**

---

## Tips

✅ **Be specific** about your requirements  
✅ **Iterate naturally** - agent remembers previous requests  
✅ **Export conversations** before clearing for project documentation  
✅ **Use prompt mode** for automation and scripting  
✅ **Check `conversation.json`** to see full message history  

---

## Help

```bash
python luna.py --help
```

---

## Example Session

```bash
# Day 1: Initial build
python luna.py prompt "Build a SaaS landing page with pricing tiers"

# Day 2: Add features
python luna.py prompt "Add FAQ accordion and testimonials carousel"

# Day 3: Refine design
python luna.py prompt "Use a gradient hero section with animated CTA"

# Export project log
python luna.py export saas_project_log.txt

# Check stats
python luna.py stats
```

**Result:** Complete website with all components, fully context-aware at every step!

---

## What's Generated

After running Luna, you'll have:

```
website_plan.md               # Project structure and requirements
component_references.md        # Found React components with code
design_specs.md               # Complete design system
src/
  components/
    Header.jsx                # All components generated
    Hero.jsx
    Features.jsx
    Footer.jsx
    ...
  App.jsx                     # Main app component
  index.css                   # Tailwind configuration
package.json                  # Project dependencies
conversation.json             # Full conversation history
```

---

## Need More Help?

📖 **Full Documentation:**
- `CONVERSATION_PERSISTENCE_GUIDE.md` - Detailed conversation features
- `PHASE_7_CONVERSATION_PERSISTENCE.md` - Implementation details
- `SETUP_GUIDE.md` - Installation and setup

🐛 **Issues?** Check `conversation.json` for debugging

🎨 **Happy Building!** Luna remembers everything. Just keep chatting!
