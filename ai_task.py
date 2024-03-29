import logging
import re
from time import sleep

import requests

piece_interface = {
    "playere": "0",
    "playerx": "1",
    "playero": "2",
}
is_spam = False

while True:
    sleep(0.5)
    text = ""

    try:
        text = requests.get(
            "http://wjm.pythonanywhere.com/wallpaper/gomoku_board/Yunzhu Li AI"
        ).text
    except:
        logging.warning("I couldn't get the game.")
        continue

    if "your turn" not in text:
        if not is_spam:
            logging.info("It's not my turn.")
            is_spam = True
        continue

    is_spam = False

    try:
        state = "".join(
            piece_interface[piece] for piece in re.findall(r"static/(\S+)\.png", text)
        )
    except:
        logging.error("I couldn't understand the response.")
        continue

    if state == "0" * 19 * 19:
        try:
            requests.post(
                f"http://wjm.pythonanywhere.com/wallpaper/gomoku/Yunzhu Li AI/180"
            )
        except:
            logging.warning("I couldn't make the move.")
            continue
    else:
        try:
            engine = requests.get(
                "https://apps.yunzhu.li/gomoku/move?s=" + state
            ).json()["result"]
        except:
            logging.error("I couldn't get the move.")
            continue

        try:
            requests.post(
                f"http://wjm.pythonanywhere.com/wallpaper/gomoku/Yunzhu Li AI/{int(engine['move_r']) * 19 + int(engine['move_c'])}"
            )
        except:
            logging.warning("I couldn't make the move.")
            continue

    logging.info("I made the move.")
