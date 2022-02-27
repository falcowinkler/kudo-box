import os

import functions_framework
from google.cloud import datastore
from slack.signature import SignatureVerifier


def verify_signature(request):
    request.get_data()  # Decodes received requests into request.data
    verifier = SignatureVerifier(os.environ['SLACK_SECRET'])
    if not verifier.is_valid_request(request.data, request.headers):
        raise ValueError('Invalid request/credentials.')


client = datastore.Client()


def persist_kudo(team_id, channel_id, team_name, channel_name, text):
    kudo_key = client.key("Team", team_id, "Channel", channel_id, "Kudo")
    entity = datastore.Entity(key=kudo_key)
    entity.update({
        "text": text
    })
    client.put(entity)


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


@functions_framework.http
def read_kudo(request):
    kudo_key = client.key(
        "Team",
        request.form["team_id"],
        "Channel",
        request.form["channel_id"],
    )
    query = client.query(kind="Kudo", ancestor=kudo_key)
    entities = list(query.fetch())
    if not entities:
        return "Error", 500
    return entities[0]["text"], 200
