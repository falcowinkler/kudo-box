import base64
import json
import os

import functions_framework
from slack.signature import SignatureVerifier

from persistence.gcloud import persist_kudo, get_kudo, delete_kudo
from render.queue import add_to_render_queue
from render.slack import upload_kudo


def verify_signature(request):
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(os.environ['SLACK_SIGNING_SECRET'])
    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')


@functions_framework.http
def write_kudo(request):
    verify_signature(request)
    persist_kudo(
        request.form['team_id'],
        request.form['channel_id'],
        request.form['team_domain'],
        request.form["channel_name"],
        request.form["text"])
    return 'Your kudo was submitted.'


def process_read_kudo_request(event, context):
    message = json.loads(base64.b64decode(event['data']))
    text = message['text']
    channel = message['channel_id']
    entity_key = message['entity_key']
    upload_kudo(channel, text)
    delete_kudo(entity_key)


@functions_framework.http
def read_kudo(request):
    verify_signature(request)
    channel_id = request.form["channel_id"]
    team_id = request.form["team_id"]
    kudo = get_kudo(team_id, channel_id)
    if not kudo:
        return "No more kudos", 200
    try:
        add_to_render_queue(channel_id, kudo)
        return "Drawing next kudo...", 200
    except Exception as e:
        return str(e), 500
