#!/usr/bin/bash

# Until Konflux shows pass/fail/error directly in webui lets exit nonzero if testing has failed.
# Easier to spot not-passing ITS this way.
echo $PRODUCED_TEST_OUTPUT | grep SUCCESS
