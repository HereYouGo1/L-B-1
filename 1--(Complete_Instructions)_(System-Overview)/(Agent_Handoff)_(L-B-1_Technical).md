# L-B-1 System - Complete Technical Documentation for Agent Handoff

## System Overview
L-B-1 (LLM Brain v1.0) is a Sequential Thinking wrapper with advanced session management, built on top of the MCP (Model Context Protocol) Sequential Thinking server. It adds persistent state management, multi-agent collaboration, and session isolation on top of the base MCP functionality.

## Core Architecture

### The Stack
1. **MCP Server** (`/Users/chrishamlin/mcp-servers/sequentialthinking-standalone/dist/index.js`)
   - Node.js server that processes thoughts
   - Actually DOES store thoughts in memory but never returns them (design flaw)
   - Spawned fresh for each thought (stateless between calls)

2. **Python Wrapper** (`/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py`)
   - Bridges to MCP server via JSON-RPC
   - Adds persistent state management
   - Implements session isolation
   - Manages contributor tracking
   - Handles briefings and context filtering

3. **State Storage** (`/Users/chrishamlin/CodingProjects/L-B-1/2--(State_Files)_(Sessions)/`)
   - Individual session JSON files in `sessions/`
   - Registry file `session_registry.json` with metadata
   - Each session tracks thoughts, contributors, branches

## Key Features Implemented

### Session Management
- **Multiple concurrent sessions** - Different projects don't mix
- **Session IDs** - User-defined or auto-generated
- **Default session** - "general" for unassigned thoughts
- **Session descriptions** - Track what each session is for
- **Migration logic** - Old single state file → new session structure

### Contributor System (Badge IDs)
- **4-character identifiers** (AG01, CH01, etc.)
- **Tracks per-contributor thought count**
- **Smart briefings** - Never shows agent their own thoughts
- **Delta updates** - Returning contributors only see new thoughts since last visit
- **Handles missing badges** - Shows as "unknown" for old thoughts

### Briefing Intelligence
- **New contributor** - Gets last 100 thoughts by default
- **Returning contributor** - Only sees thoughts added since `last_thought_number_seen`
- **Configurable** - `--show-last N` to control briefing size
- **Filtered** - Excludes caller's own thoughts to prevent duplication
- **Stderr output** - Briefings go to stderr, JSON to stdout (clean separation)

### General Session Tools
- **Partial clearing** - `--clear-general bottom-50/100/250/all`
- **Conversion** - `--convert-general BADGE_ID --convert-to SESSION_NAME`
- **Preserved metadata** - Badge IDs and timestamps maintained during conversion

## File Organization (Chris's Strict Rules)
- Folders: `(Concept_Name)_(Additional_Concepts)`
- Numbering: `0--` for README, relevance/time-based for others
- High numbers (1000) for rarely accessed items
- Every file in folder with same name
- Default file extension: `.md`

## Critical Implementation Details

### The Duplicate Storage Bug
Old wrapper stores thoughts twice:
```json
{
  "thought": "content",
  "metadata": {"thought": "content"}  // Duplicate!
}
```
This doesn't affect context but wastes disk space. Fixed in new L-B-1 wrapper.

### Context Management Issues Discovered
1. Agents only have context of what appears in chat
2. Briefings are the ONLY way to share previous thoughts
3. Decorative borders (═══) severely bloat token usage
4. Using positional arguments instead of `--stdin` causes shell escaping issues

### The CASCADE Discovery
Chris's framework mentioned Q&A checklists for concrete answers. An agent internalized this and started self-questioning, creating:
```
Q: [Question to self]
A: [Detailed answer]
Action: [Steps taken]
Cascade Effect: [Downstream impacts]
```
This emergent behavior improved reasoning quality significantly.

## Current State
- Migrated old state (18 thoughts) to "migrated-default" session
- Test session created and working
- Old wrapper at Master_Builder path has issues (corrupted state, agents using wrong format)
- New L-B-1 wrapper is stable and properly designed

## Known Issues
1. **Old wrapper state corruption** - JSON parsing errors from special characters
2. **Agents reverting to bad habits** - Using decorative borders and positional args
3. **Thought numbering confusion** - Multiple agents using different counting systems

## Git Setup
- Repository initialized at `/Users/chrishamlin/CodingProjects/L-B-1`
- Commit command: `cd /Users/chrishamlin/CodingProjects/L-B-1 && git add . && git commit -m "Updated $(date '+%Y-%m-%d %H:%M')" && git push origin master`
- Remote needs manual setup on GitHub

## Session Examples for Testing
```bash
# List sessions
python3 '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' --list-sessions

# New session with description
python3 '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' "First thought" --session-id "test-project" --badge-id AG99 --describe "Testing features"

# Continue with briefing control
python3 '/Users/chrishamlin/CodingProjects/L-B-1/1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py' "Next thought" --session-id "test-project" --badge-id AG99 --show-last 5
```
