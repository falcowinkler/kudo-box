from firebase_admin import db


def submit(text, slack_workspace_id):
    db_name = "kudos-test" if text.startswith("test:") else "kudos"

    db.reference(db_name).child(slack_workspace_id).push(
        {
            "text": text
        }
    )
