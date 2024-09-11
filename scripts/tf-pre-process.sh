#!/bin/bash -e
if [[ -n $PULL_SECRET_NAME ]]; then
    echo -n "$PULL_SECRET_NAME" > $PULL_SECRET_NAME_RESULT_PATH
else
    echo -n "imagerepository-for-${APPLICATION}-${COMPONENT}-image-pull" > $PULL_SECRET_NAME_RESULT_PATH
fi
