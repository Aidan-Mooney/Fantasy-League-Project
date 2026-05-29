from io import BytesIO
from bs4.element import Tag
from typing import Tuple


def extract_summary(match_data: Tag, team_side: str) -> Tuple[bytes, bytes]:
    """
    Extract card and substitution events for a given team from the match summary.

    This function scans the match summary HTML for events related to the
    specified team side (home or away), then builds two CSV-formatted byte
    streams:
      - one for card events (yellow, red, second yellow),
      - one for substitutions (time, player out, player in).

    Args:
        match_data (Tag): BeautifulSoup `<div>` (match summary container)
            containing cards and substitution information.
        team_side (str): Which side of the fixture this data belongs to, either
            "home" or "away".

    Returns:
        Tuple[bytes, bytes]: A tuple of two byte strings:
            - cards.csv content (time, player, card)
            - subs.csv content (time, player OUT, player IN)

    Raises:
        AttributeError: If the expected HTML structure or event breakdowns are
            missing.

    Notes:
        - Substitution entries are expected to contain "for <player>" in the
          text; this prefix is removed when extracting the incoming player.
    """
    if team_side == "home":
        html_class = "event a"
    elif team_side == "away":
        html_class = "event b"

    card_buffer = BytesIO()
    sub_buffer = BytesIO()
    card_buffer.write("time,player,card\n".encode("utf-8"))
    sub_buffer.write("time,player OUT,player IN\n".encode("utf-8"))

    raw_div = match_data.find_all("div", {"class": html_class})
    for event in raw_div:
        breakdown = [x.strip() for x in event.text.split("\n") if x.strip() != ""]
        time = breakdown[0].removesuffix("\u2019")
        event_type = breakdown[-1].removeprefix("\u2014\xa0")
        if event_type in ["Yellow Card", "Red Card", "Second Yellow Card"]:
            card_buffer.write(f"{time},{breakdown[2]},{event_type}\n".encode("utf-8"))
        elif event_type == "Substitute":
            sub_buffer.write(
                f"{time},{breakdown[2]},{breakdown[3].removeprefix('for ')}\n".encode(
                    "utf-8"
                )
            )
    return card_buffer.getvalue(), sub_buffer.getvalue()
