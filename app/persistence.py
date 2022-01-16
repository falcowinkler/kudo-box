from firebase_admin import db


def submit(text, author, slack_workspace_id):
    db_name = "kudos-test" if text.startswith("test:") else "kudos"
    workspace_database = db.reference(db_name).child(slack_workspace_id)
    all_kudos = workspace_database.get()
    # Deduplicate messages; happens when dyno starts up
    if all_kudos:
        for value in all_kudos.values():
            if 'text' in value and 'author' in value:
                if value['text'] == text and value['author'] == author:
                    return
    workspace_database.push(
        {
            "text": text,
            "author": author
        }
    )
