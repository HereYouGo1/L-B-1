# L-B-1 Situational Prompts for Chris

## Situation 1: New Agent Starting Fresh Task

### Initial Prompt
```
Navigate to /Users/chrishamlin/CodingProjects/L-B-1 and read the file:
(Agent_Instructions)_(How-To-Use-L-B-1).md

Once you understand the system, create a NEW session for our task using:
- Badge ID: [Choose unique 4-char ID like AG01]
- Session ID: [descriptive-name-here]
- Add a description of what we're working on

Use the Sequential Thinking wrapper located at:
./1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py

Begin by stating the problem/task clearly in your first thought.
```

### Session Completion Prompt (Valuable Work)
```
Great work! Please create a final summary thought in the session capturing:
1. What we accomplished
2. Key decisions made
3. Any remaining questions

Then run --history --session-id [session-name] to show me the complete record.
The session file will be preserved at:
/Users/chrishamlin/CodingProjects/L-B-1/2--(State_Files)_(Sessions)/sessions/[session-name].json
```

### Session Completion Prompt (Bullshit/Test Session)
```
This was just a test/throwaway session. Please clean it up:

1. First, verify the session name:
   python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' --list-sessions

2. Delete the session file:
   rm '/Users/chrishamlin/CodingProjects/L-B-1/2--(State_Files)_(Sessions)/sessions/[session-name].json'

3. Update the registry to remove the session:
   - Read the registry file
   - Remove the session entry
   - Save the updated registry

Be VERY careful to only delete the specific session file, not the sessions directory itself.
```

---

## Situation 2: Agent Joining Existing Session

### Standard Join Prompt
```
Navigate to /Users/chrishamlin/CodingProjects/L-B-1 and join the existing session.

First, check what sessions exist:
python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' --list-sessions

Join session "[session-name]" using:
- Your badge ID: [Choose unique ID or use assigned one]
- Session: [session-name]

IMPORTANT: When you add your first thought, you'll see a BRIEFING showing:
- Previous thoughts from OTHER agents (not your own)
- Format: "Thought X (by BADGE): content"
- This helps you understand what's already been discussed

The briefing is NOT your thoughts - it's context from others. Your thought will be added AFTER the briefing.

Start by acknowledging what you've learned from the briefing, then contribute.
```

### Returning Agent Prompt
```
You previously worked in session "[session-name]" as badge [BADGE-ID].
Return to the session to continue work.

When you add a new thought, the briefing will show:
- Only NEW thoughts from others since your last visit
- Line like: "(Showing X new thoughts since your last visit)"

This keeps you updated without repeating what you already know.
Continue from where the discussion left off.
```

---

## Situation 3: Multi-Agent Collaboration Task

### Orchestrator Prompt
```
We need multiple perspectives on this problem. Set up a collaborative session:

1. Create session with descriptive name and purpose
2. As AG01, lay out the problem/requirements
3. Switch to AG02 badge, analyze from different angle
4. Switch to AG03 badge, propose solutions
5. Return as AG01 to synthesize

Each badge switch simulates a different agent's perspective.
The briefing system will show you what each "agent" contributed.
```

---

## Situation 4: Debugging Previous Work

### Investigation Prompt
```
We need to review what happened in a previous session.

1. List all sessions to find the relevant one:
   python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' --list-sessions

2. View the full history:
   python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' --history --session-id [name]

3. If you need to continue that work, join with a new badge to add analysis
4. If it's corrupted/broken, we may need to manually edit the JSON file
```

---

## Situation 5: Complex Multiline Input

### Data/Code Input Prompt
```
You need to add code or structured data to the session. Use stdin method:

cat << 'EOF' | python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  --stdin --badge-id [YOUR-ID] --session-id [session-name]
[Paste your multiline content here]
EOF

The single quotes around EOF preserve all special characters.
This is perfect for code snippets, JSON data, or formatted text.
```

---

## Situation 6: Session Conversion/Migration

### Migration Prompt
```
We need to move thoughts from one session to another:

1. Identify the source badge and session
2. Use: --convert-general [BADGE-ID] --convert-to [new-session-name]
3. This copies all thoughts from that badge to a new session
4. Original session remains unchanged
```

---

## Situation 7: Emergency Recovery

### Corruption Recovery Prompt
```
If the wrapper fails or sessions seem corrupted:

1. Check the raw JSON files:
   ls -la '/Users/chrishamlin/CodingProjects/L-B-1/2--(State_Files)_(Sessions)/sessions/'

2. Manually inspect the problematic session:
   cat '/Users/chrishamlin/CodingProjects/L-B-1/2--(State_Files)_(Sessions)/sessions/[session].json' | python -m json.tool

3. If corrupted, either:
   - Fix the JSON manually
   - Delete and start fresh
   - Copy valid thoughts to new file

4. The registry might also need updating:
   Check: /Users/chrishamlin/CodingProjects/L-B-1/2--(State_Files)_(Sessions)/session_registry.json
```

---

## Situation 8: Quick Test/Diagnostic

### System Check Prompt
```
Test if L-B-1 is working:

python './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' \
  "System test at $(date)" \
  --badge-id TEST --session-id diagnostic-test

If you see JSON with thoughtNumber, it works.
Clean up with: rm './2--(State_Files)_(Sessions)/sessions/diagnostic-test.json'
```

---

## CRITICAL REMINDERS FOR ALL SITUATIONS

1. **Wrapper Path**: Always use './1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py'
2. **No --thought flag**: Thought is a positional argument
3. **Always use quotes**: Around paths with special characters
4. **Badge consistency**: Same badge ID across sessions for same "agent"
5. **Session names**: Lowercase with hyphens, descriptive
6. **Briefings are readonly**: They show others' thoughts, not yours
