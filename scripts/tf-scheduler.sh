#!/usr/bin/env bash
export TESTING_FARM_API_TOKEN=$(cat /etc/secrets/testing-farm-secret/testing-farm-token)

# Prepare secrets for testing farm
secrets_file=$(mktemp)
echo "AUTHFILE_b64: \"$(base64 -w 0 /etc/secrets/pull-secret-volume/.dockerconfigjson)\"" >> $secrets_file

set -x
# SNAPSHOT can contain multiple components, we are interested only in the one for 'COMPONENT'
_git_url=$(python3 -c "import os; import json; print([v for v in json.loads(os.environ['SNAPSHOT'])['components'] if v['name'] == '$COMPONENT'][0]['source']['git']['url'])")
_git_ref=$(python3 -c "import os; import json; print([v for v in json.loads(os.environ['SNAPSHOT'])['components'] if v['name'] == '$COMPONENT'][0]['source']['git']['revision'])")
_image_url=$(python3 -c "import os; import json; print([v for v in json.loads(os.environ['SNAPSHOT'])['components'] if v['name'] == '$COMPONENT'][0]['containerImage'])")
_image_name=$COMPONENT

if [[ -z "$GIT_URL" ]]; then
    GIT_URL=$_git_url
fi

# Respect explicit input
if [[ -z "$GIT_REF" ]]; then
    # Use merge/pull requests for checkout as the 'fork' might be private
    if [[ -n "$PULL_REQUEST_NUMBER" ]]; then
    case $GIT_PROVIDER in
        gitlab)
        GIT_REF="merge-requests/$PULL_REQUEST_NUMBER/head"
        ;;
        github)
        GIT_REF="pull/$PULL_REQUEST_NUMBER/head"
        ;;
        *)
        echo Unknown git_provider=$GIT_PROVIDER, use 'revision' as GIT_REF
        GIT_REF=$_git_ref
        ;;
    esac
    # "on-push" doesn't have pr/mr associated
    else
    GIT_REF=$_git_ref
    fi
fi

context_file=$(mktemp)
echo 'trigger: commit' > $context_file
echo 'initiator: konflux' >> $context_file

# Name of the snapshot
if [ -n "$SNAPSHOT_NAME" ]; then
    echo "snapshot_name: $SNAPSHOT_NAME" >> $context_file
fi

# Name of the integration test
if [ -n "$INTEGRATION_TEST_NAME" ]; then
    echo "integration_test_name: $INTEGRATION_TEST_NAME" >> $context_file
fi

tf_log=$(mktemp)

testing-farm request \
    --secret @$secrets_file \
    --environment SNAPSHOT_b64="$(echo ${SNAPSHOT} | base64 -w 0)" \
    --environment IMAGE_URL="$_image_url" \
    --environment IMAGE_NAME="$_image_name" \
    --plan "${TMT_PLAN}" \
    --context @$context_file \
    --git-url "${GIT_URL}" \
    --git-ref "${GIT_REF}" \
    --compose "${COMPOSE}" \
    --arch "${ARCH}" \
    --timeout "${TIMEOUT}" \
    --no-wait |& tee $tf_log

request_url=$(grep -oE "${TESTING_FARM_API_URL}.*$" $tf_log)
echo -n "${request_url}" > $TF_REQUEST_RESULT_PATH
