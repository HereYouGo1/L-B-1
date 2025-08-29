# How to Use the L-B-1 Sequential Thinking System - Complete Guide

## Quick Start - Where Do I Run This?

You have three options for using this system:

1. **Tell an AI agent to use it** (in their chat window)
2. **Type commands directly in Terminal/Warp** (command line)
3. **Create shortcuts/aliases** for commands you use often

## The Script Location

The main script is at:
```
/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py
```

Yes, it's a long path! You might want to create an alias (see bottom of this guide).

## Basic Command Structure

```bash
python3 [path-to-script] [optional-thought] [flags]
```

Flags always start with `--` (two dashes) or `-` (one dash for shortcuts).

## All Available Flags - Organized by Use Case

### 📝 ADDING THOUGHTS

#### Basic Thought
```bash
python3 [script] "Your thought here"
```

#### With Session ID (to organize thoughts by project)
```bash
python3 [script] "Your thought" --session-id "my-project"
```
**When to use:** Starting a new project or continuing an existing one
**What it does:** Keeps thoughts organized in separate "notebooks"

#### With Badge ID (to identify who's thinking)
```bash
python3 [script] "Your thought" --badge-id "JD01"
```
**When to use:** When multiple people/agents use the same session
**What it does:** Tracks who contributed each thought

#### Multiline Thoughts (using stdin)
```bash
python3 [script] --stdin <<'EOF'
This is line one
This is line two
This can be many lines!
EOF
```
**When to use:** When your thought is long or has multiple paragraphs
**What it does:** Lets you write thoughts without worrying about quotes

### 🗂️ SESSION MANAGEMENT

#### List All Sessions
```bash
python3 [script] --list-sessions
```
**When to use:** To see what projects/sessions exist
**What it does:** Shows all sessions with descriptions and contributor info

#### Create New Session
```bash
python3 [script] "First thought" --new-session
```
**When to use:** Starting fresh even if a default exists
**What it does:** Creates session with auto-generated ID like "sess-20240827-143022"

#### Add/Update Session Description
```bash
python3 [script] "Thought" --session-id "project-x" --describe "Working on API redesign"
```
**When to use:** To remember what each session is about
**What it does:** Adds a description to help identify sessions later

### 📖 VIEWING HISTORY

#### Show Session History
```bash
python3 [script] --history
```
**When to use:** To review all thoughts in current session
**What it does:** Displays complete thought history as JSON

#### Control Briefing Size
```bash
python3 [script] "Thought" --show-last 20
```
**When to use:** To limit how many previous thoughts you see
**What it does:** Shows only the last N thoughts (use 0 to see none)

### 🧹 CLEANUP OPERATIONS

#### Clear Entire Session
```bash
python3 [script] --clear
```
**When to use:** Starting over completely
**What it does:** Deletes the current session's state file

#### Reset Session (Keep ID)
```bash
python3 [script] "New first thought" --reset
```
**When to use:** Starting fresh but keeping the same session name
**What it does:** Clears history but keeps using the same session

#### Clear General Session
```bash
python3 [script] --clear-general bottom-50    # Clear oldest 50
python3 [script] --clear-general bottom-100   # Clear oldest 100
python3 [script] --clear-general bottom-250   # Clear oldest 250
python3 [script] --clear-general all          # Clear everything
```
**When to use:** General session getting too large
**What it does:** Removes old thoughts from the general/default session

### 🔄 CONVERSION OPERATIONS

#### Convert General to New Session
```bash
# Convert all general thoughts to new session
python3 [script] --convert-general all

# Convert only specific badge's thoughts
python3 [script] --convert-general "AG01"

# Specify the target session name
python3 [script] --convert-general "AG01" --convert-to "agent-project"
```
**When to use:** When general thoughts become a real project
**What it does:** Moves thoughts from general to a dedicated session

## Common Use Patterns

### For AI Agents

Tell your agent:
```
"Please use the sequential thinking wrapper at /Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py with:
- Session ID: 'my-project'
- Badge ID: 'AG01'
- Use --stdin for multiline thoughts
- Start with --reset if you want a clean session"
```

### For Direct Terminal Use

1. **Start a new project:**
```bash
python3 /Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py "Starting my new idea" --new-session --describe "Brainstorming app features"
```

2. **Continue existing project:**
```bash
python3 /Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py "Another thought" --session-id "sess-20240827-143022"
```

3. **Quick thought (goes to general):**
```bash
python3 /Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py "Random idea I had"
```

## Pro Tips

### Create an Alias (Shortcut)

Add this to your `~/.zshrc` or `~/.bashrc`:
```bash
alias think='python3 /Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py'
```

Then you can just type:
```bash
think "My thought here" --session-id "project"
think --list-sessions
```

### Badge ID Convention

Use a consistent format for badge IDs:
- Personal: Your initials + 01 (e.g., "JD01")
- Agents: AG + number (e.g., "AG01", "AG02")
- Friends/Family: Their initials + number

### Session Naming

Good session IDs are:
- Descriptive: "api-redesign", "birthday-planning"
- Date-based: "2024-08-project", "dec-goals"
- Project codes: "PRJ-042", "client-abc"

Avoid spaces and special characters - use hyphens instead.

## Troubleshooting

**"No such file or directory"**
- Check the path is correct
- Make sure you're using quotes around paths with special characters

**"Session not found"**
- Run `--list-sessions` to see available sessions
- Check spelling of session ID

**Seeing too many/wrong thoughts**
- Check your badge ID is set correctly
- Use `--show-last 0` to suppress briefing
- Consider using `--reset` to start fresh

## Getting Help

Run this to see all options:
```bash
python3 /Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py --help
```
