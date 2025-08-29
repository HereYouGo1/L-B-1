# L-B-1 Sequential Thinking System - Complete Instructions

## What This Is

L-B-1 (LLM Brain v1.0) is a persistent thought management system that lets AI agents collaborate on complex problems using structured sequential thinking. Think of it as a shared notebook where multiple agents can contribute thoughts, but with smart filtering so they don't get overwhelmed by irrelevant information.

## Quick Start for Different Users

### For You (Chris)

Your most common commands:
```bash
# See what sessions exist
python3 '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' --list-sessions

# Start a new project
python3 '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' "First thought" --new-session --describe "Working on X"

# Continue existing project
python3 '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' "Another thought" --session-id "project-name"
```

### For AI Agents

Standard prompt to give agents:
```
Use the Sequential Thinking wrapper at:
/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py

With these parameters:
- Session ID: [project-name]
- Badge ID: [AG01, AG02, etc.]
- Use --stdin for multiline thoughts
- Use --show-last 10 to see recent context (or 0 to suppress)
```

### For Your Dad/Girlfriend (Non-Technical Users)

1. Open Terminal/Warp
2. Copy and paste this exactly:
```bash
python3 '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' --list-sessions
```
3. This shows all available "notebooks" (sessions)
4. To add a thought, change "Your thought here" to whatever you're thinking:
```bash
python3 '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' "Your thought here"
```

## Core Concepts

### Sessions
- Like separate notebooks for different projects
- Each session keeps its thoughts isolated
- Default session: "general" (for random thoughts)
- Named sessions: "api-project", "birthday-planning", etc.

### Badge IDs
- 4-character identifier for each contributor
- Format: AG01 (agents), CH01 (Chris), JD01 (initials + number)
- Tracks who contributed what
- Prevents agents from seeing their own thoughts twice

### Briefings
- When a new agent/badge joins, they see previous thoughts
- Smart filtering: doesn't show their own previous thoughts
- Configurable: --show-last N (or 0 to suppress)
- New badges see last 100, returning badges see only new thoughts

## Common Workflows

### Starting a New Project

```bash
# Agent or human starting fresh
python3 [script] "Project kickoff thought" --new-session --describe "Building new API" --badge-id CH01
```

### Multi-Agent Collaboration

```bash
# Agent 1 starts
python3 [script] "Analyzing requirements" --session-id "api-v2" --badge-id AG01 --stdin <<'EOF'
[Detailed multi-line thought]
EOF

# Agent 2 continues (sees AG01's thoughts)
python3 [script] "Building on AG01's analysis" --session-id "api-v2" --badge-id AG02

# Agent 1 returns (only sees new thoughts from AG02)
python3 [script] "Response to AG02" --session-id "api-v2" --badge-id AG01
```

### Converting General to Project

```bash
# After random thoughts become a real project
python3 [script] --convert-general AG01 --convert-to "new-project"
```

### Cleaning Up

```bash
# Clear old thoughts from general session
python3 [script] --clear-general bottom-100

# Reset a session completely
python3 [script] --clear --session-id "old-project"
```

## Session Management Features

### List All Sessions
Shows descriptions, contributors, thought counts
```bash
python3 [script] --list-sessions
```

### Create Named Session
```bash
python3 [script] "First thought" --session-id "my-project" --describe "Working on X"
```

### View Session History
```bash
python3 [script] --history --session-id "my-project"
```

### General Session Management
- Automatic fallback for thoughts without session ID
- Can be cleared partially (bottom-50, bottom-100, bottom-250)
- Can convert badge-specific thoughts to new sessions

## Advanced Features

### Controlling Context Size

Problem: 220-thought projects can blow up context
Solution: Use badges and filtering

```bash
# New agent joining large project - limit briefing
python3 [script] "Continuing work" --session-id "big-project" --badge-id AG99 --show-last 20

# Same conversation continuing - no briefing needed
python3 [script] "Next thought" --session-id "big-project" --badge-id AG99 --show-last 0
```

### The Q&A Thinking Style

Your CASCADE framework accidentally created a powerful pattern. Agents structure thoughts as:
```
Q: [Question to self]
A: [Detailed answer]
Action: [What to do]
Cascade Effect: [Downstream impacts]
```

To preserve this style, tell agents: "Continue using the Q&A self-questioning format from the CASCADE framework"

### Avoiding Context Explosion

DON'T:
- Use decorative borders (══════)
- Echo full thoughts back in chat
- Use huge totalThoughts numbers unnecessarily

DO:
- Use --show-last wisely
- Keep session-specific badges
- Let wrapper manage state (don't dump JSONs in chat)

## File Locations

```
L-B-1/
├── 0--(README_Folder)/                          # Overview
├── 0.1--(Flags_Documentation)_(How-To-Guide)/   # All flags explained
├── 1--(Complete_Instructions)_(System-Overview)/ # This file
├── 2--(State_Files)_(Sessions)/                 # Where thoughts are stored
│   ├── sessions/                                # Individual session files
│   └── session_registry.json                    # Session metadata
└── 1000--(Py-WPR)_(ST)_(L-B-1)/                # The actual Python script
```

## Troubleshooting

### "Session not found"
- Check spelling with --list-sessions
- Sessions are case-sensitive

### Context getting too large
- Use --show-last with smaller number
- Use different badge IDs for different conversation threads
- Consider breaking into multiple sessions

### Agent not seeing previous thoughts
- Check they're using different badge ID than the original author
- Verify --show-last isn't set to 0
- Make sure session ID matches

### Want to start completely fresh
```bash
# Nuclear option - clear everything
python3 [script] --clear --session-id "session-name"

# Or for general session
python3 [script] --clear-general all
```

## The Migration from Old System

Your old state file (with 500+ thoughts) was migrated to "migrated-default" session. The original file still exists at the old location if needed.

## For Your Other Projects

When continuing your 220-thought CASCADE project:
1. Use new badge (AG22 instead of AG99) to see all previous thoughts
2. Remove decorative borders going forward
3. Use --stdin properly (not positional arguments)
4. Keep Q&A style but without the ══════ lines

## Future Action Items System (Coming Soon)

The next evolution: turning agent actions into testable LEGO blocks that can be debugged and improved based on failure patterns. Stay tuned!
