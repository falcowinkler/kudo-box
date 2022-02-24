gcloud functions deploy write_kudo \
--runtime python39 \
--trigger-http \
--set-env-vars "SLACK_SECRET=${SLACK_SIGNING_SECRET}" \
--allow-unauthenticated