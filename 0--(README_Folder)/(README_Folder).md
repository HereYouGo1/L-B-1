# L-B-1 (LLM Brain v1.0) - Project Structure

## What's In Here?
The folders within this directory contain the core components of the LLM Brain system. You'll find Python scripts that act as bridges to the MCP (Model Context Protocol) server, as well as systems for managing persistent thought storage and session tracking. The folders are ordered by relevance and likely usage frequency - the stuff you'll need most often comes first, with the deep technical bits pushed down to higher numbers.

## Directory Structure

### 1000--(Py-WPR)_(ST)_(L-B-1)
Contains the main Python wrapper script that bridges to the Sequential Thinking MCP server. This script manages:
- Session-based thought persistence
- Multi-agent collaboration via badge IDs
- Contributor tracking and thought attribution
- General session for unassigned thoughts
- Session conversion and management utilities

### 2--(State_Files)_(Sessions)
Stores all session data and the session registry:
- `sessions/` - Individual session JSON files
- `session_registry.json` - Metadata about all sessions including descriptions, contributors, and thought counts

## Key Features

1. **Session Management**
   - Multiple concurrent sessions with unique IDs
   - General session for unassigned thoughts
   - Session descriptions and metadata tracking

2. **Multi-Agent Collaboration**
   - Badge ID system for agent identification
   - Contributor tracking with thought counts
   - Smart briefing that excludes agent's own thoughts
   - Delta updates for returning contributors

3. **General Session Tools**
   - Clear oldest thoughts (50, 100, 250, or all)
   - Convert badge-specific thoughts to new sessions
   - Preserve metadata and attribution

4. **Migration Support**
   - Automatic migration from old single-state format
   - Preserves existing thought history

## Usage

See the Python wrapper help for detailed usage:
```bash
python3 1000--(Py-WPR)_(ST)_(L-B-1)/(Py-WPR)_(ST)_(L-B-1).py --help
```

## Git Commands

To commit and push changes:
```bash
cd /Users/chrishamlin/CodingProjects/L-B-1 && git add . && git commit -m "Updated $(date '+%Y-%m-%d %H:%M')" && git push origin master
```
