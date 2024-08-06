#!/usr/bin/env python3
import requests
import sys
import time  
import json


SLEEP = 60

previous_state = None

retry_adapter = requests.HTTPAdapter(max_retries=requests.Retry(total=10,
                backoff_factor=0.2))
session = requests.Session()
session.mount('http://', retry_adapter)
session.mount('https://', retry_adapter)

while True:
    ret = session.get(sys.argv[1]).json()
    state = ret['state']
    if state == previous_state:
        print('.', end=None, file=sys.stderr)
    else:
        if previous_state is not None:
            print()
        print(f'{state=}', file=sys.stderr)
        previous_state = state
    if state not in ['new', 'queued', 'running']:
        print(f'Stop waiting as {state=}', file=sys.stderr)
        break
    time.sleep(SLEEP) 

f_out = sys.argv[2]
with open(f_out, 'w') as f:
    json.dump(ret, f)
print(f'Wrote requests json to "{f_out}"', file=sys.stderr)    
