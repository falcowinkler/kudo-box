import base64
import json
import logging
import os
from collections import namedtuple
from http import HTTPStatus

import functions_framework
import slack
from slack.signature import SignatureVerifier

import encryption.kudos as kudos_encryption
from persistence.gcloud import persist_kudo, delete_kudo, get_credentials, persist_bot_token, get_all_kudos, \
    flag_box_as_being_opened, is_box_being_opened
from render.queue import create_read_kudo_topic, add_read_all_command_to_queue
from render.render_to_slack import render_and_upload_kudo, post_initial_message

Kudo = namedtuple("Kudo", ["text", "key"])


def verify_signature(request):
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(os.environ['SLACK_SIGNING_SECRET'])
    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')


@functions_framework.http
def write_kudo(request):
    verify_signature(request)
    team_id = request.form['team_id']
    if get_credentials(team_id) is None:
        return authorization_error_message(request.form["team_domain"])
    password = get_password()
    encrypted_kudo = kudos_encryption.encrypt(request.form["text"], password)
    persist_kudo(
        team_id,
        request.form['channel_id'],
        encrypted_kudo)
    return 'Your kudo got created in the box for #' + request.form['channel_name']


def get_text(kudos_present):
    if kudos_present:
        return "Today's kudos in the thread 🧵!"
    return "There are no kudos in the kudo-box for this channel."


def process_read_kudo_request(event, context):
    message = json.loads(base64.b64decode(event['data']))
    channel_id = message['channel_id']
    team_id = message['team_id']
    credentials = get_credentials(team_id)
    kudos = get_all_kudos(team_id, channel_id)
    kudos_present = len(kudos) > 0
    thread_ts = post_initial_message(channel_id, credentials, get_text(kudos_present))
    flag_box_as_being_opened(team_id, channel_id, True)
    try:
        for encrypted_kudo in get_all_kudos(team_id, channel_id):
            kudo = decrypt_kudo(encrypted_kudo)
            render_and_upload_kudo(channel_id, kudo.text, credentials, thread_ts)
            delete_kudo(kudo.key)
    except Exception as e:
        logging.error(e)
    flag_box_as_being_opened(team_id, channel_id, False)


@functions_framework.http
def open_kudo_box(request):
    verify_signature(request)
    team_id = request.form["team_id"]
    channel_id = request.form["channel_id"]
    if is_box_being_opened(team_id, channel_id):
        return "Box is already being opened. Wait until all kudos are read, then try again", 200
    if get_credentials(team_id) is None:
        return authorization_error_message(request.form["team_domain"])
    try:
        add_read_all_command_to_queue(team_id, channel_id)
        return "Drawing all kudos...", 200
    except Exception as e:
        render_queue_not_found = hasattr(e, "code") and e.code == HTTPStatus.NOT_FOUND
        if render_queue_not_found:
            create_read_kudo_topic()
            return open_kudo_box(request)
        return str(e), 500


@functions_framework.http
def read_kudo(request):
    return open_kudo_box(request)


def decrypt_kudo(encrypted_kudo):
    password = get_password()
    kudo = Kudo(kudos_encryption.decrypt(encrypted_kudo.token, password), encrypted_kudo.key)
    return kudo


def authorization_error_message(team_domain):
    scopes = "channels:join,chat:write,commands,files:write"
    client_id = os.getenv("SLACK_CLIENT_ID")
    oauth_link = f"https://{team_domain}.slack.com/oauth/v2/authorize?client_id={client_id}&scope={scopes}"
    return f'Authorization Error. Please <a href="{oauth_link}">click here</a> to authorize.', 403


def get_password():
    return os.getenv("ENCRYPTION_SECRET")


@functions_framework.http
def oauth_redirect(request):
    code = request.args['code']
    response = oauth_access(code)
    team_id = response['team']['id']
    access_token = response['access_token']
    persist_bot_token(team_id, access_token)
    return "All done! You can start writing Kudos now"


def oauth_access(code):
    client = slack.WebClient()
    client_id = os.environ['SLACK_CLIENT_ID']
    client_secret = os.environ['SLACK_CLIENT_SECRET']
    response = client.oauth_v2_access(
        client_id=client_id,
        client_secret=client_secret,
        code=code
    )
    return response
