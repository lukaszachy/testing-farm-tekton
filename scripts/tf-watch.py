#!/usr/bin/env python3
import requests
import sys
import time  
import json

while True:
    ret = requests.get(sys.argv[1]).json()
    state = ret['state']
    print(f'{state=}', file=sys.stderr)
    if state not in ['new', 'queued', 'running']:
        print(f'Stop waiting as {state=}', file=sys.stderr)
        break
    print(time.gmtime(), file=sys.stderr)
    time.sleep(60) 

f_out = sys.argv[2]
with open(f_out, 'w') as f:
    json.dump(ret, f)
print(f'Wrote requests json to "{f_out}"', file=sys.stderr)    
