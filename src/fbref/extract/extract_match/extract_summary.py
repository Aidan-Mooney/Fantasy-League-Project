from io import BytesIO


def extract_summary(match_data, team_side):
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
