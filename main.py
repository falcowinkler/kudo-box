import base64
import json
import os
from collections import namedtuple

import functions_framework
from slack.signature import SignatureVerifier

from persistence.gcloud import persist_kudo, get_kudo, delete_kudo, get_bot_token, persist_bot_token
from render.queue import add_to_render_queue
from render.slack import render_and_upload_kudo
import encryption.kudos as kudos_encryption

Kudo = namedtuple("Kudo", ["text", "key"])


def verify_signature(request):
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(os.environ['SLACK_SIGNING_SECRET'])
    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')


@functions_framework.http
def write_kudo(request):
    verify_signature(request)
    password = derive_password(request)
    encrypted_kudo = kudos_encryption.encrypt(request.form["text"], password)
    persist_kudo(
        request.form['team_id'],
        request.form['channel_id'],
        encrypted_kudo)
    return 'Your kudo was submitted.'


def process_read_kudo_request(event, context):
    message = json.loads(base64.b64decode(event['data']))
    text = message['text']
    channel = message['channel_id']
    entity_key = message['entity_key']
    render_and_upload_kudo(channel, text)
    delete_kudo(entity_key)


@functions_framework.http
def read_kudo(request):
    verify_signature(request)
    team_id = request.form["team_id"]
    channel_id = request.form["channel_id"]
    encrypted_kudo = get_kudo(team_id, channel_id)
    if not encrypted_kudo:
        return "No more kudos", 200
    password = derive_password(request)
    kudo = Kudo(kudos_encryption.decrypt(encrypted_kudo.token, password), encrypted_kudo.key)
    try:
        add_to_render_queue(channel_id, kudo)
        return "Drawing next kudo...", 200
    except Exception as e:
        return str(e), 500


def derive_password(request):
    return kudos_encryption.make_password(
        request.form['team_domain'],
        request.form["channel_name"],
        os.getenv("ENCRYPTION_SECRET")
    )


@functions_framework.http
def oauth_redirect(request):
    code = request.args.get('code')
    response = oauth_access(code)
    team_id = response['team_id']
    persist_bot_token(team_id, response)


def oauth_access(code):
    data = {
        'code': code,
    }

    auth = (
        os.environ['SLACK_CLIENT_ID'].encode('utf-8'),
        os.environ['SLACK_CLIENT_SECRET'].encode('utf-8')
    )

    resp = requests.post(
        "https://slack.com/api/oauth.access",
        data=data,
        auth=auth
    )

    return resp.json()
