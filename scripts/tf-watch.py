#!/usr/bin/env python3
import requests
import sys
import time          

while True:
    ret = requests.get(sys.argv[1]).json()
    state = ret['state']
    print(f'{state=}', file=sys.stderr)
    if state not in ['new', 'queued', 'running']:
        print(f'Stop waiting, becasue {state=}', file=sys.stderr)
        break
    print(time.gmtime(), file=sys.stderr)
    time.sleep(60) 

# not running...
if state != 'complete':
    print('Not completed job!', file=sys.stderr)
    raise SystemExit(2)
    
overal_result = ret['result']['overall']
print(f'{overal_result=}', file=sys.stderr)

if overal_result != 'passed':
    print('Not passed', file=sys.stderr)
    raise SystemExit(1)

