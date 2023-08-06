import sys
import html

import requests

from blocks import clean, title


def focused(on, no_scripts=True, to_file=True):
    # Set headers
    headers = {"user-agent": "focused"}

    # Get website
    response = requests.get(
        on,
        headers=headers
    )
    if response.status_code != 200:
        raise Exception(f"[{response.status_code}]")

    # Remove comments and scripts
    head, body = clean(response.text, no_scripts)

    # Compose web page and unescape html entites
    page = html.unescape(f"<!DOCTYPE html>\n<html>\n{head}\n{body}\n</html>")

    if to_file:
        with open(f"{title(head)}.html", "w") as file:
            file.write(page)
    else:
        return page


if __name__ == "__main__":
    focused(on=sys.argv[1])
