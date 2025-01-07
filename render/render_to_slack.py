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
    mentioned = ", ".join(extract_mentions(text))
    file_path = create_card(readable_mentions(text))
    slack_client = WebClient(token=credentials.bot_token)
    try:
        slack_client.conversations_join(channel=channel)
    except:  # already in channel
        pass
    response = slack_client.files_upload_v2(
        channel=channel,
        file=file_path,
        thread_ts=thread_ts,
        filename="kudos.gif",
        initial_comment=random_comment(),
        title=random_title())

    def extract_ts(lst):
        return [info["ts"] for info in lst]

    def extract_shares(dct):
        return [t for lst in dct.values() for t in extract_ts(lst)]

    private_shares = extract_shares(response["file"]["shares"].get("private", {}))
    public_shares = extract_shares(response["file"]["shares"].get("public", {}))
    shares = private_shares + public_shares
    if mentioned:
        for thread_ts in shares:
            slack_client.api_call(
                'chat.postMessage',
                data={
                    'channel': channel,
                    'thread_ts': thread_ts,
                    'text': mentioned
                }
            )
