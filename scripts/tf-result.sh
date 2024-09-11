#!/usr/bin/bash

# Until Konflux shows pass/fail/error directly in webui lets exit nonzero if testing has failed.
# Easier to spot not-passing ITS this way.
grep SUCCESS  "$1" < /dev/null
