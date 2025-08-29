import pandas as pd  # Unused import
import numpy  # Missing 'as np' convention
# Missing import for 'json' but used below

def process_data(data):
    # Using undefined variable
    result = clean_data(user_data)  # user_data is undefined
    
    # Missing return statement in some paths
    if result:
        return result
    # No else return!

def helper_function():
    # This function is never called (unused)
    pass

# Using undefined function
output = transform_data(input_data)  # both undefined

# Using module that wasn't imported
json_output = json.dumps(output)  # json not imported

# Syntax issue (in some Python versions)
print "Old style print"  # Python 2 style in Python 3

# Variable used before definition
print(final_result)
final_result = "Done"
