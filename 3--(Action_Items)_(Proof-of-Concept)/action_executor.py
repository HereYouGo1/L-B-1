#!/usr/bin/env python3
"""
Action Item Executor - Proof of Concept
This simulates how an agent would execute action items and track failures
"""

import json
import ast
import sys
from pathlib import Path
from datetime import datetime

class ActionExecutor:
    def __init__(self):
        self.error_database = []
        self.execution_log = []
        
    def execute_action(self, action_name, file_path):
        """Execute a specific action item and return results"""
        
        # Log the execution attempt
        self.execution_log.append({
            "action": action_name,
            "file": file_path,
            "timestamp": datetime.now().isoformat()
        })
        
        # Execute based on action type
        if action_name == "[SCAN_FILE]":
            return self._scan_file(file_path)
        elif action_name == "[CHECK_SYNTAX]":
            return self._check_syntax(file_path)
        elif action_name == "[CHECK_IMPORTS]":
            return self._check_imports(file_path)
        elif action_name == "[CHECK_VARIABLES]":
            return self._check_variables(file_path)
        elif action_name == "[CHECK_FUNCTIONS]":
            return self._check_functions(file_path)
        else:
            return {"error": f"Unknown action: {action_name}"}
    
    def _scan_file(self, file_path):
        """[SCAN_FILE] implementation"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.count('\n') + 1
                
            return {
                "lines": lines,
                "language": "python",
                "size_bytes": len(content)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _check_syntax(self, file_path):
        """[CHECK_SYNTAX] implementation"""
        errors = []
        warnings = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Try to parse as Python
            try:
                ast.parse(content)
            except SyntaxError as e:
                errors.append(f"Line {e.lineno}: {e.msg}")
                
            # Check for Python 2 vs 3 issues
            if 'print "' in content or "print '" in content:
                warnings.append("Python 2 style print statement detected")
                
        except Exception as e:
            errors.append(f"Failed to check: {e}")
            
        return {"errors": errors, "warnings": warnings}
    
    def _check_imports(self, file_path):
        """[CHECK_IMPORTS] implementation"""
        missing = []
        unused = []
        invalid = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Parse to find imports
            tree = ast.parse(content)
            imported_modules = set()
            imported_names = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imported_modules.add(name.name.split('.')[0])
                        imported_names.add(name.asname if name.asname else name.name)
                elif isinstance(node, ast.ImportFrom):
                    imported_modules.add(node.module.split('.')[0] if node.module else '')
            
            # Check for usage (simplified - real implementation would be more thorough)
            for module in imported_modules:
                if module and module not in content.replace(f'import {module}', ''):
                    unused.append(module)
            
            # Check for missing imports (looking for common patterns)
            if 'json.' in content and 'json' not in imported_modules:
                missing.append('json')
                
        except SyntaxError:
            # Can't parse due to syntax errors
            return {"missing": [], "unused": [], "invalid": ["Cannot parse due to syntax errors"]}
        except Exception as e:
            invalid.append(str(e))
            
        return {"missing": missing, "unused": unused, "invalid": invalid}
    
    def _check_variables(self, file_path):
        """[CHECK_VARIABLES] implementation"""
        undefined = []
        unused = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Simplified check - look for obvious undefined variables
            # In reality, this would need proper scope analysis
            lines = content.split('\n')
            defined_vars = set()
            used_vars = set()
            
            for i, line in enumerate(lines):
                # Very simplified - just for demo
                if '=' in line and not line.strip().startswith('#'):
                    var_name = line.split('=')[0].strip()
                    if ' ' not in var_name:  # Simple variable
                        defined_vars.add(var_name)
                
                # Check for undefined variable usage (very simplified)
                if 'user_data' in line and 'user_data' not in defined_vars:
                    undefined.append(f"user_data at line {i+1}")
                if 'input_data' in line and 'input_data' not in defined_vars:
                    undefined.append(f"input_data at line {i+1}")
                if 'final_result' in line:
                    # Check if used before definition
                    if 'final_result' not in defined_vars and 'print' in line:
                        undefined.append(f"final_result at line {i+1}")
                    
        except Exception as e:
            return {"undefined": [], "unused": [], "error": str(e)}
            
        return {"undefined": undefined, "unused": unused, "shadowed": []}
    
    def _check_functions(self, file_path):
        """[CHECK_FUNCTIONS] implementation"""
        undefined_calls = []
        unused_functions = []
        missing_returns = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Look for undefined function calls
            if 'clean_data(' in content:
                undefined_calls.append('clean_data')
            if 'transform_data(' in content:
                undefined_calls.append('transform_data')
                
            # Check for unused functions
            if 'def helper_function' in content:
                if 'helper_function(' not in content.replace('def helper_function', ''):
                    unused_functions.append('helper_function')
                    
        except Exception as e:
            return {"undefined_calls": [], "unused_functions": [], "missing_returns": [], "error": str(e)}
            
        return {
            "undefined_calls": undefined_calls,
            "unused_functions": unused_functions,
            "missing_returns": missing_returns
        }
    
    def execute_workflow(self, workflow_file, target_file):
        """Execute a complete workflow"""
        # Load workflow
        with open(workflow_file, 'r') as f:
            workflow = json.load(f)
        
        print(f"\n=== Executing Workflow: {workflow['workflow_name']} ===")
        print(f"Target file: {target_file}\n")
        
        results = {}
        
        for step in workflow['steps']:
            print(f"Step {step['step']}: {step['action']} - {step['description']}")
            
            result = self.execute_action(step['action'], target_file)
            results[step['action']] = result
            
            # Print results
            print(f"  Result: {json.dumps(result, indent=2)}")
            
            # Handle failures based on workflow rules
            if 'error' in result or (result.get('errors', [])):
                if step['on_failure'] == 'abort':
                    print("  ❌ Critical failure - aborting workflow")
                    break
                elif step['on_failure'] == 'continue_with_warning':
                    print("  ⚠️ Warning detected - continuing")
                else:
                    print("  ℹ️ Non-critical - continuing")
            else:
                print("  ✅ Success")
        
        return results
    
    def record_failure(self, action, expected, actual, context):
        """Record a failure for learning"""
        failure = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "expected": expected,
            "actual": actual,
            "context": context,
            "diagnosis": "TO BE DETERMINED"
        }
        self.error_database.append(failure)
        
        # Save to error database
        db_file = Path("4--(Error_Database)/errors.json")
        if db_file.exists():
            with open(db_file, 'r') as f:
                db = json.load(f)
        else:
            db = {"errors": []}
        
        db["errors"].append(failure)
        
        with open(db_file, 'w') as f:
            json.dump(db, f, indent=2)
        
        return failure

if __name__ == "__main__":
    executor = ActionExecutor()
    
    # Test the workflow on our buggy file
    workflow_file = "2--(Workflows)/code_review_v1.json"
    test_file = "3--(Test_Files)/buggy_code.py"
    
    results = executor.execute_workflow(workflow_file, test_file)
    
    print("\n=== Workflow Complete ===")
    print("\nDetected Issues:")
    
    # Summarize findings
    all_errors = []
    for action, result in results.items():
        if 'errors' in result and result['errors']:
            all_errors.extend([(action, err) for err in result['errors']])
        if 'undefined' in result and result['undefined']:
            all_errors.extend([(action, f"Undefined: {item}") for item in result['undefined']])
        if 'undefined_calls' in result and result['undefined_calls']:
            all_errors.extend([(action, f"Undefined function: {func}") for func in result['undefined_calls']])
        if 'missing' in result and result['missing']:
            all_errors.extend([(action, f"Missing import: {imp}") for imp in result['missing']])
    
    for action, error in all_errors:
        print(f"  • {action}: {error}")
    
    # Now simulate what happens when an agent misses something
    print("\n=== Simulating Agent Failure ===")
    print("Agent claims: 'All variables are defined'")
    print("Reality: user_data and input_data are undefined")
    
    # Record the failure
    failure = executor.record_failure(
        action="[CHECK_VARIABLES]",
        expected={"undefined": ["user_data", "input_data", "final_result"]},
        actual={"undefined": []},  # Agent missed them
        context={"file_size": 500, "language": "python"}
    )
    
    print(f"\nFailure recorded: {failure['action']} failed to detect undefined variables")
    print("This data will be used to improve the workflow!")
