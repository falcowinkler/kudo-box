import render.emoji_mapping


def test_emoji_mapping(mocker):
    mocker.patch("render.emoji_mapping.load_lookup", return_value={
        "smiling_face": {"unified": "1F972"},
        "sad_face": {"unified": "1F932-1F3FF"},
    })
    text = "Great work! :smiling_face::sad_face:"
    result = "Great work! 🥲🤲🏿"
    assert render.emoji_mapping.replace_emojis(text) == result
