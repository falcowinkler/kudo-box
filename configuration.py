import os
import json

with open(os.getenv("CONFIG_FILE"), "r") as config_file:
    config = json.load(config_file)
    config["firebaseServiceaccount"]["private_key"] = os.getenv("SERVICEACCOUNT_PRIVATE_KEY").encode("utf-8").decode(
        'unicode_escape')
    config["slackConfig"] = {
        "slack_signing_secret": os.getenv("SLACK_SIGNING_SECRET"),
        "slack_bot_token": os.getenv("SLACK_BOT_TOKEN"),
    }
