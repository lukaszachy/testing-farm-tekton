#!/usr/bin/env python3
import requests
import sys
import time  
import json

first_dot=False

SLEEP = 60

while True:
    ret = requests.get(sys.argv[1]).json()
    state = ret['state']
    print(f'{state=}', file=sys.stderr)
    if state not in ['new', 'queued', 'running']:
        print(f'\nStop waiting as {state=}', file=sys.stderr)
        break
    if first_dot:
        print(f"Sleep {SLEEP}s between checks", end='', file=sys.stderr)
    print('.', end='',file=sys.stderr)
    time.sleep(SLEEP) 

f_out = sys.argv[2]
with open(f_out, 'w') as f:
    json.dump(ret, f)
print(f'Wrote requests json to "{f_out}"', file=sys.stderr)    
