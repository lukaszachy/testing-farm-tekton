#!/usr/bin/env python3
import requests
import sys
import time
import json
from requests.adapters import HTTPAdapter, Retry


SLEEP = 60

previous_state = None

retry_adapter = HTTPAdapter(max_retries=Retry(total=10,
                backoff_factor=0.2))
session = requests.Session()
session.mount('http://', retry_adapter)
session.mount('https://', retry_adapter)

print(f'Each dot is {SLEEP} seconds')

while True:
    ret = session.get(sys.argv[1]).json()
    state = ret['state']
    if state == previous_state:
        print('.', end='', file=sys.stderr, flush=True)
    else:
        if previous_state is not None:
            print()
        print(f'{state=} ', file=sys.stderr, end='', flush=True)
        previous_state = state
    if state not in ['new', 'queued', 'running']:
        print('\nStop waiting, final state.', file=sys.stderr)
        break
    time.sleep(SLEEP)

f_out = sys.argv[2]
with open(f_out, 'w') as f:
    json.dump(ret, f)
print(f'Wrote requests json to "{f_out}"', file=sys.stderr)
