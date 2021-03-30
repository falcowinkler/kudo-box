import hashlib
import hmac
import os
import random
import threading

from firebase_admin import db
from flask import request
from slack import WebClient

import app.firebase_submit as firebase
from app import app, slack_config
from app.render import create_card

slack_bot_token = slack_config["slack_bot_token"]


def verify_slack_request():
    slack_signature = request.headers['X-Slack-Signature']
    slack_request_timestamp = request.headers['X-Slack-Request-Timestamp']
    request_body = request.get_data()
    slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")
    basestring = f"v0:{slack_request_timestamp}:".encode('utf-8') + request_body
    slack_signing_secret = bytes(slack_signing_secret, 'utf-8')
    my_signature = 'v0=' + hmac.new(slack_signing_secret, basestring, hashlib.sha256).hexdigest()
    return hmac.compare_digest(my_signature, slack_signature)


@app.route('/write_kudo_card', methods=['POST'])
def write_card():
    if verify_slack_request():
        kudo_text = request.values['text']
        author = request.values['user_name']
        slack_workspace_id = request.values['team_id']
        firebase.submit(kudo_text, author, slack_workspace_id)
        return "Your kudo was submitted"
    return "Security checks failed"


def random_title():
    return random.choice([
        "Here's a sticker",
        "Sorry, you don't get a medal though",
        "Makes a great wall decoration!",
        "You get this designer-approved card!",
        "You get this tacky card as a reward.",
        "+5 jollity",
        "Show it to all your friends!",
        "Consider the environment before printing.",
        "For your trophy collection:"
    ])


def random_comment():
    return random.choice([
        "Good job!",
        "Way to go, kiddo",
        "WTG!",
        "What would we do without you",
        "Great success!",
        "Nice!",
        "Noice!",
        "Sweet",
        "Dandy",
        "Sweet n' dandy"
    ])


def open_card(slack_request):
    client = WebClient(token=slack_bot_token)
    text = slack_request['text']
    team_id = slack_request['team_id']
    database = "kudos-test" if text == "test" else "kudos"
    channel = slack_request["channel_id"]
    kudos = db.reference(database).child(team_id)
    items = kudos.order_by_key().limit_to_first(1).get()
    if items is None:
        client.chat_postMessage(
            channel=channel,
            text="no more kudos")
    else:
        items = list(items.items())
        key, value = items[0]
        text = value["text"]
        file_path = create_card(text)
        client.api_call("files.upload",
                        files={
                            "file": file_path
                        },
                        data={
                            'channels': channel,
                            'filename': "kudos.png",
                            'title': random_title(),
                            'initial_comment': random_comment(),
                        }
                        )
        kudos.child(key).delete()


@app.route("/read_kudo_card", methods=['POST'])
def handle_message():
    if verify_slack_request():
        download_thread = threading.Thread(target=open_card, args=[request.values])
        download_thread.start()
        return '', 200
