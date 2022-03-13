if [ -z ${SLACK_SIGNING_SECRET+x} ]; then
  echo "SLACK_SIGNING_SECRET is not set as environment variable"
  exit 1
fi

gcloud functions deploy write_kudo \
--runtime python39 \
--trigger-http \
--set-env-vars "SLACK_SECRET=${SLACK_SIGNING_SECRET}" \
--allow-unauthenticated