import re
from typing import List


def extract_mentions(text: str) -> List[str]:
    return [f"<@{identifier}>" for identifier in re.findall("<@([A-Z0-9]+)\\|.*?>", text)]


def readable_mentions(text: str) -> str:
    return re.sub("<@[A-Z0-9]+\\|(.*?)>", lambda match: f"@{match.group(1)}", text)
