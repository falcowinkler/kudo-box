#!/usr/bin/env bash
set -euo pipefail
if [ -z ${SLACK_SIGNING_SECRET+x} ]; then
  echo "SLACK_SIGNING_SECRET is not set as environment variable"
  exit 1
fi

if [ -z ${ENCRYPTION_SECRET+x} ]; then
  echo "ENCRYPTION_SECRET is not set as environment variable"
  exit 1
fi

gcloud functions deploy write_kudo \
--runtime python39 \
--min-instances 1 \
--trigger-http \
--set-env-vars "SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}" \
--set-env-vars "ENCRYPTION_SECRET=${ENCRYPTION_SECRET}" \
--allow-unauthenticated