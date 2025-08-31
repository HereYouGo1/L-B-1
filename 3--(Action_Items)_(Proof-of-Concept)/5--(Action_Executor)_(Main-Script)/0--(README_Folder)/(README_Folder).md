# Action Executor - The Main Test Script

## What The Fuck Is This?

This is the MAIN SCRIPT that demonstrates how the Action Items system works. It's a Python script that simulates how LLM agents would execute your "LEGO block" action items and track their failures.

## How To Run It

```bash
cd /Users/chrishamlin/CodingProjects/L-B-1/3--(Action_Items)_(Proof-of-Concept)
python '5--(Action_Executor)_(Main-Script)/(Action_Executor)_(Main-Script).py'
```

## What It Does

1. **Loads the workflow** from `2--(Workflows)/code_review_v1.json`
2. **Executes each action** defined in `1--(Action_Definitions)/action_items.json`
3. **Runs against test file** in `3--(Test_Files)/buggy_code.py`
4. **Records failures** to `4--(Error_Database)/errors.json`

## What You'll See When You Run It

```
=== Executing Workflow: CodeReview_v1 ===
Target file: 3--(Test_Files)/buggy_code.py

Step 1: [SCAN_FILE] - Get file metadata
  Result: {"lines": 30, "language": "python", "size_bytes": 745}
  ✅ Success

Step 2: [CHECK_SYNTAX] - Validate syntax first
  Result: {"errors": ["Line 25: invalid syntax"], "warnings": ["Python 2 style print"]}
  ⚠️ Warning detected - continuing

[... continues through all 5 steps ...]

=== Simulating Agent Failure ===
Agent claims: 'All variables are defined'
Reality: user_data and input_data are undefined
Failure recorded: [CHECK_VARIABLES] failed to detect undefined variables
```

## The Key Parts Inside

- **`execute_action()`** - Runs individual action items
- **`execute_workflow()`** - Chains actions together
- **`record_failure()`** - Captures when agents fuck up
- **`_check_variables()`, `_check_syntax()`, etc.** - Individual action implementations

## Why This Matters

This executor PROVES your concept works:
- Actions can be deterministic and testable
- Workflows chain properly
- Failures can be tracked precisely
- The same error patterns will emerge across projects

## To Modify/Extend

1. Add new action methods (like `_check_security()`)
2. Update the workflow JSON to include new steps
3. Create new test files with different bug patterns
4. Run repeatedly to build error pattern database

This is the HEART of your proof of concept - it shows that breaking LLM tasks into atomic, trackable actions actually works.
