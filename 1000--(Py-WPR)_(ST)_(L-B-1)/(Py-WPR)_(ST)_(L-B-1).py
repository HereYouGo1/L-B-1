#!/usr/bin/env python3
"""
Sequential Thinking with Session-Based State Persistence
Maintains thought history across calls in session-specific JSON files
L-B-1 (LLM Brain v1.0)
"""

import json
import subprocess
import sys
import uuid
import os
import argparse
import shutil
from datetime import datetime
from pathlib import Path

# Base directories
BASE_DIR = Path("/Users/chrishamlin/CodingProjects/L-B-1")
STATE_DIR = BASE_DIR / "2--(State_Files)_(Sessions)" / "sessions"
REGISTRY_FILE = BASE_DIR / "2--(State_Files)_(Sessions)" / "session_registry.json"

# MCP server path
MCP_SERVER_PATH = "/Users/chrishamlin/mcp-servers/sequentialthinking-standalone/dist/index.js"

# Ensure directories exist
STATE_DIR.mkdir(parents=True, exist_ok=True)

def load_registry():
    """Load the session registry"""
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, 'r') as f:
            return json.load(f)
    return {
        "sessions": {},
        "default_session": None
    }

def save_registry(registry):
    """Save the session registry"""
    with open(REGISTRY_FILE, 'w') as f:
        json.dump(registry, f, indent=2)

def get_session_file(session_id):
    """Get the path to a session state file"""
    return STATE_DIR / f"{session_id}.json"

def load_state(session_id):
    """Load the current thinking state from session file"""
    session_file = get_session_file(session_id)
    if session_file.exists():
        with open(session_file, 'r') as f:
            return json.load(f)
    return {
        "thought_history": [],
        "branches": {},
        "current_thought_number": 0,
        "session_id": session_id,
        "created_at": datetime.now().isoformat()
    }

def save_state(state, session_id):
    """Save the current thinking state to session file"""
    session_file = get_session_file(session_id)
    with open(session_file, 'w') as f:
        json.dump(state, f, indent=2)

def update_registry_for_session(session_id, state, description=None):
    """Update registry metadata for a session"""
    registry = load_registry()
    
    # Count contributors and their thoughts
    contributor_thoughts = {}
    for thought in state.get("thought_history", []):
        badge = thought.get("badge_id", "unknown")
        contributor_thoughts[badge] = contributor_thoughts.get(badge, 0) + 1
    
    # Update session info
    if session_id not in registry["sessions"]:
        registry["sessions"][session_id] = {
            "created_at": state.get("created_at", datetime.now().isoformat()),
            "description": description or f"Session {session_id}"
        }
    
    registry["sessions"][session_id].update({
        "last_modified": datetime.now().isoformat(),
        "contributor_count": len(contributor_thoughts),
        "thought_count": len(state.get("thought_history", [])),
        "contributors": contributor_thoughts,
        "description": description or registry["sessions"][session_id].get("description", "")
    })
    
    save_registry(registry)

def determine_session_id(args):
    """Determine which session to use based on arguments and existing state"""
    registry = load_registry()
    
    # If explicit session ID provided
    if args.session_id:
        return args.session_id
    
    # If forcing new session
    if args.new_session:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"sess-{timestamp}"
    
    # Check for default session in registry
    if registry.get("default_session"):
        return registry["default_session"]
    
    # Default to general session
    return "general"

def list_sessions():
    """List all available sessions with metadata"""
    registry = load_registry()
    
    if not registry["sessions"]:
        print("No sessions found.")
        return
    
    print("\n=== Available Sessions ===")
    for session_id, info in registry["sessions"].items():
        print(f"\n📁 {session_id}")
        if session_id == registry.get("default_session"):
            print("   ⭐ DEFAULT SESSION")
        print(f"   Description: {info.get('description', 'No description')}")
        print(f"   Created: {info.get('created_at', 'Unknown')[:10]}")
        print(f"   Modified: {info.get('last_modified', 'Unknown')[:10]}")
        print(f"   Thoughts: {info.get('thought_count', 0)}")
        print(f"   Contributors: {info.get('contributor_count', 0)}")
        
        # Show contributor breakdown
        contributors = info.get('contributors', {})
        if contributors:
            sorted_contributors = sorted(contributors.items(), key=lambda x: x[1], reverse=True)
            print("   Contributors breakdown:")
            for badge, count in sorted_contributors[:5]:  # Show top 5
                print(f"      - {badge}: {count} thoughts")
            if len(sorted_contributors) > 5:
                print(f"      ... and {len(sorted_contributors) - 5} more")

def clear_general_session(option):
    """Clear thoughts from the general session"""
    session_file = get_session_file("general")
    if not session_file.exists():
        print("No general session found.")
        return
    
    state = load_state("general")
    original_count = len(state["thought_history"])
    
    if option == "all":
        state["thought_history"] = []
        state["current_thought_number"] = 0
        print(f"Cleared all {original_count} thoughts from general session.")
    else:
        # Extract number from option (e.g., "bottom-50" -> 50)
        try:
            count = int(option.split("-")[1])
            if len(state["thought_history"]) <= count:
                state["thought_history"] = []
                state["current_thought_number"] = 0
                print(f"Cleared all {original_count} thoughts from general session.")
            else:
                # Keep only the newest thoughts
                state["thought_history"] = state["thought_history"][count:]
                print(f"Cleared oldest {count} thoughts from general session. {len(state['thought_history'])} remaining.")
        except (ValueError, IndexError):
            print(f"Invalid clear option: {option}")
            return
    
    save_state(state, "general")
    update_registry_for_session("general", state)

def convert_general_to_session(badge_id=None, new_session_id=None):
    """Convert general session thoughts to a new session, optionally filtered by badge"""
    general_file = get_session_file("general")
    if not general_file.exists():
        print("No general session found.")
        return
    
    general_state = load_state("general")
    
    # Filter thoughts if badge_id provided
    if badge_id:
        filtered_thoughts = [t for t in general_state["thought_history"] if t.get("badge_id") == badge_id]
        if not filtered_thoughts:
            print(f"No thoughts found for badge {badge_id} in general session.")
            return
    else:
        filtered_thoughts = general_state["thought_history"]
    
    if not filtered_thoughts:
        print("No thoughts to convert.")
        return
    
    # Generate session ID if not provided
    if not new_session_id:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        new_session_id = f"converted-{badge_id}-{timestamp}" if badge_id else f"converted-{timestamp}"
    
    # Create new session
    new_state = {
        "thought_history": filtered_thoughts,
        "branches": {},
        "current_thought_number": max([t.get("number", 0) for t in filtered_thoughts], default=0),
        "session_id": new_session_id,
        "created_at": datetime.now().isoformat()
    }
    
    # Copy participant info if it exists
    if "participants" in general_state:
        new_state["participants"] = {}
        if badge_id:
            if badge_id in general_state["participants"]:
                new_state["participants"][badge_id] = general_state["participants"][badge_id]
        else:
            new_state["participants"] = general_state["participants"].copy()
    
    save_state(new_state, new_session_id)
    update_registry_for_session(new_session_id, new_state, 
                               f"Converted from general session" + (f" (badge {badge_id})" if badge_id else ""))
    
    # Remove converted thoughts from general session
    if badge_id:
        general_state["thought_history"] = [t for t in general_state["thought_history"] 
                                          if t.get("badge_id") != badge_id]
    else:
        general_state["thought_history"] = []
        general_state["current_thought_number"] = 0
    
    save_state(general_state, "general")
    update_registry_for_session("general", general_state)
    
    print(f"Converted {len(filtered_thoughts)} thoughts to new session: {new_session_id}")
    return new_session_id

def send_sequential_thought(thought, session_id, thought_number=None, total_thoughts=1, next_thought_needed=False,
                           is_revision=None, revises_thought=None, branch_from_thought=None, 
                           branch_id=None, needs_more_thoughts=None, reset=False, badge_id=None, 
                           show_last=None, description=None):
    """Send a thought and maintain state across calls"""
    
    # Load or reset state
    if reset:
        state = {
            "thought_history": [],
            "branches": {},
            "current_thought_number": 0,
            "session_id": session_id,
            "created_at": datetime.now().isoformat()
        }
    else:
        state = load_state(session_id)

    # Participants tracking (keeping old name internally for compatibility)
    if "participants" not in state:
        state["participants"] = {}

    # Track the highest thought number currently in the session (before adding new one)
    current_highest_thought = max([t.get("number", 0) for t in state.get("thought_history", [])], default=0)
    
    # Determine if this badge is new to the session
    is_new_badge = False
    last_seen_thought_number = 0
    if badge_id:
        if badge_id not in state["participants"]:
            is_new_badge = True
            state["participants"][badge_id] = {
                "first_seen_at": datetime.now().isoformat(),
                "thoughts_authored": 0,
                "last_thought_number_seen": current_highest_thought  # They've now seen everything up to this point
            }
        else:
            # Get the last thought number this badge saw
            last_seen_thought_number = state["participants"][badge_id].get("last_thought_number_seen", 0)

    # Decide how many prior thoughts to show
    if show_last is None:
        if is_new_badge:
            show_last = 100  # New badge: show last 100
        else:
            show_last = -1  # Returning badge: show all since last visit (handled below)

    # Print previous thoughts as a briefing for the agent
    if state.get("thought_history") and show_last != 0:
        # Filter out the caller's own thoughts if a badge_id is provided
        filtered_history = [t for t in state["thought_history"] if (not badge_id) or (t.get("badge_id") != badge_id)]
        
        if show_last == -1:
            # Returning badge: show all thoughts since last visit
            to_show = [t for t in filtered_history if t.get("number", 0) > last_seen_thought_number]
        else:
            # Explicit count or new badge: show last N
            to_show = filtered_history[-show_last:] if show_last > 0 else []
        
        if to_show:
            print(f"--- Briefing: Previous Thoughts in Session '{session_id}' ---", file=sys.stderr)
            for thought_item in to_show:
                who = thought_item.get("badge_id") or "unknown"
                print(f"  Thought {thought_item.get('number')} (by {who}): {thought_item.get('thought')}", file=sys.stderr)
            
            if show_last == -1:
                print(f"--- (Showing {len(to_show)} new thoughts since your last visit; total in session: {len(state['thought_history'])}) ---\n", file=sys.stderr)
            else:
                print(f"--- (Showing last {len(to_show)} of {len(filtered_history)} from others; total in session: {len(state['thought_history'])}) ---\n", file=sys.stderr)
    
    # Auto-increment thought number if not specified
    if thought_number is None:
        state["current_thought_number"] += 1
        thought_number = state["current_thought_number"]
    else:
        state["current_thought_number"] = thought_number
    
    # Build arguments
    arguments = {
        "thought": thought,
        "thoughtNumber": thought_number,
        "totalThoughts": total_thoughts,
        "nextThoughtNeeded": next_thought_needed
    }
    
    if is_revision is not None:
        arguments["isRevision"] = is_revision
    if revises_thought is not None:
        arguments["revisesThought"] = revises_thought
    if branch_from_thought is not None:
        arguments["branchFromThought"] = branch_from_thought
    if branch_id is not None:
        arguments["branchId"] = branch_id
        if branch_id not in state["branches"]:
            state["branches"][branch_id] = []
    if needs_more_thoughts is not None:
        arguments["needsMoreThoughts"] = needs_more_thoughts
    
    # Store thought in history
    thought_entry = {
        "number": thought_number,
        "thought": thought,
        "timestamp": datetime.now().isoformat(),
        "metadata": arguments,
        "badge_id": badge_id,
        "session_id": session_id
    }
    state["thought_history"].append(thought_entry)
    
    if branch_id:
        state["branches"][branch_id].append(thought_entry)
    
    # Update participants authored count and last seen
    if badge_id:
        state["participants"][badge_id]["thoughts_authored"] = state["participants"].get(badge_id, {}).get("thoughts_authored", 0) + 1
        # Update to the current thought number (they've now seen everything including their own new thought)
        state["participants"][badge_id]["last_thought_number_seen"] = thought_number
    
    # Save state and update registry
    save_state(state, session_id)
    update_registry_for_session(session_id, state, description)
    
    # Create the JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tools/call",
        "params": {
            "name": "sequentialthinking",
            "arguments": arguments
        }
    }
    
    # Start a fresh MCP server process (stateless on server side)
    process = subprocess.Popen(
        ["node", MCP_SERVER_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Initialize
    init_request = {
        "jsonrpc": "2.0",
        "id": "init",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "wrapper", "version": "1.0.0"}
        }
    }
    
    process.stdin.write(json.dumps(init_request) + "\n")
    process.stdin.flush()
    init_response = process.stdout.readline()
    
    process.stdin.write('{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
    process.stdin.flush()
    
    # Send thought request
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    
    # Read response
    response = process.stdout.readline()
    process.terminate()
    
    # Parse response
    result = json.loads(response) if response else None
    
    # Enhance response with our state
    if result:
        response_data = json.loads(result['result']['content'][0]['text'])
        response_data['thoughtHistoryLength'] = len(state["thought_history"])
        response_data['branches'] = list(state["branches"].keys())
        response_data['sessionId'] = session_id
        result['result']['content'][0]['text'] = json.dumps(response_data, indent=2)
    
    return result

def get_thought_history(session_id):
    """Get the full thought history for a session"""
    state = load_state(session_id)
    return state["thought_history"]

def clear_session(session_id):
    """Clear a specific session state file"""
    session_file = get_session_file(session_id)
    if session_file.exists():
        os.remove(session_file)
        
        # Remove from registry
        registry = load_registry()
        if session_id in registry["sessions"]:
            del registry["sessions"][session_id]
            if registry.get("default_session") == session_id:
                registry["default_session"] = None
            save_registry(registry)
        
        print(f"Session '{session_id}' cleared")
    else:
        print(f"Session '{session_id}' not found")

def migrate_old_state():
    """Migrate old single state file to new session structure"""
    old_state_file = Path("/Users/chrishamlin/CodingProjects/Master_Builder/Main_Agents/MASTER_BUILDER/***Agent_Hopper/ST_New_Python_Access/Agent_State_Logs/sequential_thinking_state.json")
    
    if old_state_file.exists():
        print("🔄 Migrating old state file to new session structure...", file=sys.stderr)
        
        with open(old_state_file, 'r') as f:
            old_state = json.load(f)
        
        # Save as default session
        save_state(old_state, "migrated-default")
        update_registry_for_session("migrated-default", old_state, "Migrated from old state file")
        
        # Set as default session
        registry = load_registry()
        registry["default_session"] = "migrated-default"
        save_registry(registry)
        
        print(f"✅ Migration complete! Old state moved to session 'migrated-default'", file=sys.stderr)
        print(f"   Original file preserved at: {old_state_file}", file=sys.stderr)
        return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sequential Thinking bridge with session-based state persistence. L-B-1 (LLM Brain v1.0)"
    )
    parser.add_argument("thought", nargs="?", help="Thought text (ignored if --stdin or --input-file is used)")
    parser.add_argument("thought_number", nargs="?", type=int, help="Explicit thought number (optional)")
    parser.add_argument("total_thoughts", nargs="?", type=int, help="Estimated total thoughts (optional)")

    # Session management
    parser.add_argument("--session-id", help="Specify session ID (default: 'general')")
    parser.add_argument("--new-session", action="store_true", help="Force create a new session")
    parser.add_argument("--list-sessions", action="store_true", help="List all available sessions")
    parser.add_argument("--describe", help="Add/update session description")
    
    # General session management
    parser.add_argument("--clear-general", choices=["bottom-50", "bottom-100", "bottom-250", "all"],
                       help="Clear thoughts from general session")
    parser.add_argument("--convert-general", help="Convert general session to new session (optionally specify badge ID)")
    parser.add_argument("--convert-to", help="Specify session ID for conversion (use with --convert-general)")
    
    # Existing flags
    parser.add_argument("--history", action="store_true", help="Show full thought history for session")
    parser.add_argument("--clear", action="store_true", help="Clear the current session")
    parser.add_argument("--reset", action="store_true", help="Start a fresh session before sending the thought")
    parser.add_argument("--stdin", action="store_true", help="Read the thought from standard input (multi-line supported)")
    parser.add_argument("--input-file", "-f", help="Read the thought from a file path (multi-line supported)")
    parser.add_argument("--badge-id", help="4-character badge id for the calling agent (used to filter briefing)")
    parser.add_argument("--show-last", type=int, help="How many prior thoughts to show in briefing (0 to suppress)")
    
    args = parser.parse_args()

    # Check for migration on first run
    if not REGISTRY_FILE.exists():
        migrate_old_state()

    # Handle list sessions
    if args.list_sessions:
        list_sessions()
        sys.exit(0)
    
    # Handle clear general
    if args.clear_general:
        clear_general_session(args.clear_general)
        sys.exit(0)
    
    # Handle convert general
    if args.convert_general:
        badge_id = args.convert_general if args.convert_general != "all" else None
        new_session_id = args.convert_to
        convert_general_to_session(badge_id, new_session_id)
        sys.exit(0)
    
    # Determine session
    session_id = determine_session_id(args)
    
    # Handle history
    if args.history:
        history = get_thought_history(session_id)
        print(f"=== Session '{session_id}' History ===")
        print(json.dumps(history, indent=2))
        sys.exit(0)
    
    # Handle clear
    if args.clear:
        clear_session(session_id)
        sys.exit(0)

    # Determine thought source
    thought_text = None
    if args.stdin:
        thought_text = sys.stdin.read()
    elif args.input_file:
        try:
            with open(args.input_file, "r") as fh:
                thought_text = fh.read()
        except Exception as e:
            print(f"Failed to read --input-file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.thought is not None:
        thought_text = args.thought

    if args.reset and not thought_text:
        print("Need thought when using --reset (provide via positional arg, --stdin, or --input-file)")
        sys.exit(1)

    if thought_text is None:
        print("Usage: python3 (Python_Wrapper)_(Sequential-Thinking).py '<thought>' [thought_number] [total_thoughts]")
        print("       python3 (Python_Wrapper)_(Sequential-Thinking).py --stdin < <file_or_heredoc>")
        print("       python3 (Python_Wrapper)_(Sequential-Thinking).py --input-file path.txt")
        print("\nSession Management:")
        print("       --session-id NAME      Join/create specific session")
        print("       --new-session          Force create new session")
        print("       --list-sessions        Show all sessions")
        print("       --describe 'text'      Add session description")
        print("\nGeneral Session:")
        print("       --clear-general [bottom-50|bottom-100|bottom-250|all]")
        print("       --convert-general BADGE_ID  Convert badge's thoughts to new session")
        print("       --convert-to SESSION_ID     Specify target session for conversion")
        print("\nOther Commands:")
        print("       --history              Show session history")
        print("       --clear                Clear current session")
        print("       --badge-id XXXX        Set agent badge ID")
        sys.exit(1)

    thought_number = args.thought_number if args.thought_number is not None else None
    total_thoughts = args.total_thoughts if args.total_thoughts is not None else 10
    next_needed = True

    result = send_sequential_thought(
        thought_text,
        session_id=session_id,
        thought_number=thought_number,
        total_thoughts=total_thoughts,
        next_thought_needed=next_needed,
        reset=args.reset,
        badge_id=args.badge_id,
        show_last=args.show_last,
        description=args.describe
    )

    if result:
        print(json.dumps(result, indent=2))
