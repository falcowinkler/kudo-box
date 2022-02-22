from collections import namedtuple

import functions_framework
from google.cloud import datastore

client = datastore.Client()

Persistence = namedtuple("persistence", ["write_kudo", "read_kudo"])


def make_persistence(db):
    def _write_kudo(team_id, channel_id, team_name, channel_name, text):
        # TODO: (this is just an example)
        key = db.key("Dog", "Freddie")
        entity = datastore.Entity(key=key)
        entity.update({
            "Breed": "Border Collie",
            "Age": 2,
            "Loves": "Swimming",
        })
        db.put(entity)

        result = db.get(key)
        print(result)

    return Persistence(
        write_kudo=_write_kudo,
        read_kudo=None  # TODO
    )


ds_client = datastore.Client()
persistence = make_persistence(ds_client)


@functions_framework.http
def write_kudo(request):
    persistence.write_kudo("team_id", "channel_id", "team_name", "channel_name", "text")
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    return f'Hello World!'
