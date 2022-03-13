#!/usr/bin/env bash
set -euo pipefail

if [ -z ${GOOGLE_CLOUD_PROJECT+x} ]; then
  echo "GOOGLE_CLOUD_PROJECT is not set as environment variable"
  exit 1
fi

if [ -z ${SLACK_BOT_TOKEN+x} ]; then
  echo "SLACK_BOT_TOKEN is not set as environment variable"
  exit 1
fi

gcloud functions deploy process_read_kudo_request \
--runtime python39 \
--set-env-vars "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
--set-env-vars "SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}" \
--trigger-topic read-kudo-queue