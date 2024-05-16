#!/usr/bin/env python3

import json
import sys

def write_js(obj, f_path):
    with open(f_path, 'w') as f:
        json.dump(obj, f)
def write(obj, f_path):
    with open(f_path, 'w') as f:
        f.write(str(obj))

with open(sys.argv[1]) as f:
    request = json.load(f)

f_artifacts_url = sys.argv[2]
f_test_output = sys.argv[3]

# Report the URL to artifacts
artifacts = request['run']['artifacts']
if artifacts:
    write(artifacts, f_artifacts_url) 

# Process the results..
test_output = {
    'result': 'ERROR',
    "timestamp": request['updated'],
    "successes": 0, 
    "failures": 0,
    "warnings": 0
}
    

state = request['state']    
if state != 'complete':
    test_output['note'] = f'TF request finished as {state}'
overall = request['result']['overall']

# Nothing will create 'WARNING'
overall2tekton = {
'passed': 'SUCCESS',
'failed': 'FAILURE',
'skipped': 'SKIPPED',
'error': 'ERROR',
'unknown': 'ERROR',
}

test_output['result'] = overall2tekton[overall]
write_js(test_output, f_test_output)

if overall != 'passed':
    raise SystemExit(1)
