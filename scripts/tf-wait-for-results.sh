#!/usr/bin/env bash
request_outcome=$(mktemp)

echo "Will be checking $TF_REQUEST ..."
if [[ -z $TF_REQUEST ]]; then
    echo Nothing to check
    exit 1
fi

# Watch until request finishes
/usr/local/bin/tf-watch.py $TF_REQUEST $request_outcome

# Parse and make the output
/usr/local/bin/tf-parse.py $request_outcome $ARTIFACTS_URL_RESULT_PATH $TEST_OUTPUT_RESULT_PATH
