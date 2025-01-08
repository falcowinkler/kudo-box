from slack_sdk import WebClient

from render.image import create_card
from render.text import random_title, random_comment
from render.mentions import extract_mentions, readable_mentions


def post_initial_message(channel, credentials, text):
    slack_client = WebClient(token=credentials.bot_token)
    response = slack_client.api_call(
        'chat.postMessage',
        data={
            'channel': channel,
            'text': text
        }
    )
    return response["ts"]


def render_and_upload_kudo(channel, text, credentials, thread_ts=None):
    mentions = extract_mentions(text)
    mentioned = "\n" + ", ".join(mentions)
    file_path = create_card(readable_mentions(text))
    slack_client = WebClient(token=credentials.bot_token)
    try:
        slack_client.conversations_join(channel=channel)
    except:  # already in channel
        pass
    slack_client.files_upload_v2(
        channel=channel,
        file=file_path,
        thread_ts=thread_ts,
        filename="kudos.gif",
        initial_comment=random_comment() + mentioned if mentions else "",
        title=random_title())
