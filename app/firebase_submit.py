from app import db


def submit(sender, receiver, text, access_token):
    db_name = "kudos-test" if text.startswith("test:") else "kudos"

    db.child(db_name).push(
        {
            "sender": sender,
            "receiver": receiver,
            "text": text
        },
        token=access_token
    )
