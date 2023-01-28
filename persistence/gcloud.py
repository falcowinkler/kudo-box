import random
from collections import namedtuple

from google.cloud import datastore

EncryptedKudo = namedtuple("EncryptedKudo", ["token", "key"])
Credentials = namedtuple("Credentials", ["bot_token"])

client = datastore.Client()


def persist_kudo(team_id, channel_id, encrypted_text):
    kudo_key = client.key("Team", team_id, "Channel", channel_id, "Kudo")
    entity = datastore.Entity(key=kudo_key)
    entity.update({
        "token": encrypted_text
    })
    client.put(entity)


def get_all_kudos(team_id, channel_id):
    kudo_key = client.key(
        "Team",
        team_id,
        "Channel",
        channel_id
    )
    query = client.query(kind="Kudo", ancestor=kudo_key)
    entities = list(query.fetch())
    return [
        EncryptedKudo(entity['token'], entity.key.flat_path)
        for entity in entities
    ]


def get_kudo(team_id, channel_id):
    """returns random (text, key) if any kudo exists in the box or None otherwise."""
    all_kudos = get_all_kudos(team_id, channel_id)
    if len(all_kudos) > 0:
        return random.choice(
            get_all_kudos(team_id, channel_id)
        )


def delete_kudo(kudo_key):
    client.delete(client.key(*kudo_key))


def get_credentials(team_id):
    query = client.query(kind="Credentials")
    query.add_filter("team_id", "=", team_id)

    entities = list(query.fetch())
    if not entities:
        return

    return Credentials(entities[0]['bot_token'])


def persist_bot_token(team_id, bot_token):
    bot_key = client.key("Credentials", team_id)
    entity = datastore.Entity(key=bot_key)
    entity.update({
        "team_id": team_id,
        "bot_token": bot_token
    })
    client.put(entity)
