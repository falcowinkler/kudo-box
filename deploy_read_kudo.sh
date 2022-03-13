if [ -z ${SLACK_SIGNING_SECRET+x} ]; then
  echo "SLACK_SIGNING_SECRET is not set as environment variable"
  exit 1
fi

if [ -z ${SLACK_BOT_TOKEN+x} ]; then
  echo "SLACK_BOT_TOKEN is not set as environment variable"
  exit 1
fi


gcloud functions deploy read_kudo \
--runtime python39 \
--trigger-http \
--set-env-vars "SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}" \
--set-env-vars "SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}" \
--allow-unauthenticated