from render.mentions import extract_mentions, readable_mentions


def test_mentions():
    text = "to <@U012ABCDEF|user1> for giving a birthday cake to <@U345GHIJKL|user2>"
    assert extract_mentions(text) == ["<@U012ABCDEF>", "<@U345GHIJKL>"]


def test_readable_mentions():
    text = "to <@U012ABCDEF|user1> for giving a birthday cake to <@U345GHIJKL|user2>"
    assert readable_mentions(text) == "to @user1 for giving a birthday cake to @user2"
