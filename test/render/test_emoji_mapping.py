from render.emoji_mapping import *


def test_emoji_mapping():
    text = "Great work! :slightly_smiling_face::flag-it::it:"
    result = "Great work! 🙂🇮🇹🇮🇹"
    assert replace_emojis(text) == result


def test_skin_tones():
    text = "Great work! :+1::+1::skin-tone-2::+1::skin-tone-3::+1::skin-tone-4::+1::skin-tone-5::+1::skin-tone-6:"
    result = "Great work! 👍👍🏻👍🏼👍🏽👍🏾👍🏿"
    assert replace_emojis(text, parse_skin_tones=True) == result


def test_emoji_split():
    text = "Great work! 🙂🇮🇹🇮🇹"
    result = ["Great", "work!", "🙂", "🇮🇹", "🇮🇹"]
    assert split_str_and_emojis(text) == result
