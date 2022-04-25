#!/usr/bin/env bash
set -euo pipefail
if [ -z ${SLACK_SIGNING_SECRET+x} ]; then
  echo "SLACK_SIGNING_SECRET is not set as environment variable"
  exit 1
fi

if [ -z ${GOOGLE_CLOUD_PROJECT+x} ]; then
  echo "GOOGLE_CLOUD_PROJECT is not set as environment variable"
  exit 1
fi

if [ -z ${ENCRYPTION_SECRET+x} ]; then
  echo "ENCRYPTION_SECRET is not set as environment variable"
  exit 1
fi

gcloud functions deploy read_kudo \
--runtime python39 \
--trigger-http \
--set-env-vars "SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}" \
--set-env-vars "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
--set-env-vars "ENCRYPTION_SECRET=${ENCRYPTION_SECRET}" \
--allow-unauthenticated