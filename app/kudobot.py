import random
import textwrap
import threading
import uuid

import firebase_admin
from PIL import Image, ImageFont, ImageDraw
from firebase_admin import credentials
from firebase_admin import db
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from app import app
from app import firebase_config
from app import serviceaccount_config
from app import slack_config

cred = credentials.Certificate(serviceaccount_config)
firebase_admin.initialize_app(cred, {
    'databaseURL': firebase_config['databaseURL']
})


def create_card(sender, receiver, text):
    text = f"""\
From: {sender}
To: {receiver}
---
{text}"""

    font_path = 'fonts/MostlyMono.ttf'
    num_images = 9
    image = random.randint(1, num_images)
    x = Image.open(f'images/{image}.png').convert('RGB')
    # thank you card TODO: text is over image if too long
    lines = textwrap.wrap(text, width=30 if image not in [4,
                                                          5] else 45)
    font = ImageFont.truetype(font_path, 28, encoding='unic')
    y_text = 130
    draw = ImageDraw.Draw(x)
    for line in lines:
        width, height = font.getsize(line)
        draw.text((30, y_text), line, font=font, fill=(0, 0, 0))
        y_text += height + 10
    filename = f"generated/{uuid.uuid4()}.png"
    x.save(filename)
    return filename


# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = slack_config["slack_signing_secret"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events", app)

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = slack_config["slack_bot_token"]


def process(event_data):
    client = WebClient(token=slack_bot_token)
    text = event_data['event']['text']
    if "read" in text:
        database = "kudos-test" if "test" in text else "kudos"
        message = event_data["event"]
        # If the incoming message contains "hi", then respond with a "Hello" message
        channel = message["channel"]
        kudos = db.reference(database)
        items = kudos.order_by_key().limit_to_first(1).get()
        if items is None:
            client.chat_postMessage(
                channel=channel,
                text="no more kudos")
        else:
            items = list(items.items())
            key, value = items[0]
            sender, receiver, text = value["sender"], value["receiver"], value["text"]
            file_path = create_card(sender, receiver, text)
            client.api_call("files.upload",
                            files={
                                "file": file_path
                            },
                            data={
                                'channels': channel,
                                'filename': "kudos.png",
                                'title': f'Great job!',
                                'initial_comment': f'Kudos to {receiver}!',
                            }
                            )
            kudos.child(key).delete()


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    download_thread = threading.Thread(target=process, args=[event_data])
    download_thread.start()
    return {"isBase64Encoded": True, "statusCode": 200, "headers": {}, "body": ""}
