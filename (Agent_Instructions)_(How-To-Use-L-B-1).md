# Agent Instructions - How to Use L-B-1 Sequential Thinking

## Quick Start for Agents

You're an agent who needs to use the L-B-1 Sequential Thinking system. Here's everything you need to know.

### The Wrapper Location
The Python wrapper is NOT at the root. It's here:
```bash
/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py
```

### Your First Command
```bash
python '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' "Your thought here" --badge-id AG01 --session-id your-session
```

**IMPORTANT:** The thought is a POSITIONAL argument, not a flag. Don't use `--thought`.

---

## Essential Concepts

### 1. Badge ID (Your Identity)
Every agent needs a unique badge ID. This tracks WHO is thinking.
- Format: 2-4 characters (e.g., AG01, XY99, TEST)
- Stays consistent across sessions
- Example: `--badge-id AG01`

### 2. Session ID (Your Workspace)
Sessions are isolated conversation spaces. Multiple agents can collaborate in one session.
- Format: lowercase with hyphens (e.g., debug-task, main-analysis)
- Creates automatically if doesn't exist
- Example: `--session-id debug-task`

### 3. The Briefing System
When you join a session, you automatically see:
- Thoughts from OTHER badges (not your own)
- Only new thoughts since your last visit
- Helps you catch up on what you missed

---

## Common Tasks

### Join a Session and Add a Thought
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "Analyzing the error in module X" \
  --badge-id AG01 \
  --session-id debug-session
```

### Add a Multiline Thought (Method 1: Direct)
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "Line 1 of thought
Line 2 of thought
Line 3 of thought" \
  --badge-id AG01 \
  --session-id debug-session
```

### Add a Multiline Thought (Method 2: stdin)
```bash
cat << 'EOF' | python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  --stdin --badge-id AG01 --session-id debug-session
This is a complex multiline thought.
It can contain "quotes" and special characters.
Even JSON: {"key": "value"}
EOF
```

### View Session History
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  --history --session-id debug-session
```

### List All Available Sessions
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' --list-sessions
```

### Create Session with Description
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "Starting new debugging task" \
  --badge-id AG01 \
  --session-id new-debug \
  --describe "Debugging the authentication module"
```

---

## Multi-Agent Collaboration Example

### Agent 1 Starts
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "Found bug in line 42 of auth.py" \
  --badge-id AG01 --session-id bug-fix
```

### Agent 2 Joins and Sees Briefing
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "I see the bug AG01 found. Testing a fix now." \
  --badge-id AG02 --session-id bug-fix
```
Output includes:
```
--- Briefing: Previous Thoughts in Session 'bug-fix' ---
  Thought 1 (by AG01): Found bug in line 42 of auth.py
```

### Agent 1 Returns and Sees Update
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "Great! What fix did you try?" \
  --badge-id AG01 --session-id bug-fix
```
Output includes:
```
--- Briefing: Previous Thoughts in Session 'bug-fix' ---
  Thought 2 (by AG02): I see the bug AG01 found. Testing a fix now.
--- (Showing 1 new thoughts since your last visit) ---
```

---

## Important Flags Reference

| Flag | Purpose | Example |
|------|---------|---------|
| `--badge-id` | Your unique identifier | `--badge-id AG01` |
| `--session-id` | Session to join/create | `--session-id main-task` |
| `--stdin` | Read thought from stdin | `echo "thought" \| ... --stdin` |
| `--history` | View session history | `--history --session-id main` |
| `--list-sessions` | See all sessions | `--list-sessions` |
| `--describe` | Add session description | `--describe "Purpose here"` |
| `--show-last` | Limit briefing size | `--show-last 5` |
| `--clear` | Clear current session | `--clear --session-id main` |

---

## Where Files Are Stored

Sessions are saved in:
```
/Users/chrishamlin/CodingProjects/L-B-1/2--(State_Files)_(Sessions)/sessions/
```

Each session is a JSON file named `{session-id}.json`

---

## Common Mistakes to Avoid

### ❌ WRONG - Using --thought flag
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  --thought "This won't work"  # WRONG!
```

### ✅ CORRECT - Thought as positional argument
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "This will work"  # CORRECT!
```

### ❌ WRONG - Forgetting quotes around path
```bash
python ./1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py  # Shell will fail
```

### ✅ CORRECT - Path in quotes
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py'  # Works!
```

### ❌ WRONG - No badge ID
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "Thought" --session-id main  # Who are you?
```

### ✅ CORRECT - Always include badge
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "Thought" --badge-id AG01 --session-id main
```

---

## Quick Diagnostic Test

Run this to verify the system works:
```bash
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "Test thought from $(date)" \
  --badge-id TEST --session-id test-session
```

If you see a JSON response with `thoughtNumber`, it's working!