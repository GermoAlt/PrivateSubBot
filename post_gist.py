import json

import requests

from config import github


def make_gist(contents):
    r = requests.post(
        "https://api.github.com/gists",
        auth=github,
        data=json.dumps(
            {
                "description": "Comments for entry.",
                "public": False,
                "files": {"comments_for_entry.md": {"content": contents}},
            }
        ),
    )
    response = r.content.decode("utf-8")
    response_json = json.loads(response)
    return response_json["html_url"]
