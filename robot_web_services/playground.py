#!/usr/bin/env python

import os
import pathlib
import requests
import requests.auth
import requests.sessions
import sys


config = {
    "url_base": "http://localhost:80/"
}


def main() -> int:
    file = pathlib.Path(__file__)
    os.chdir(file.parent)

    with open(".secrets/api.key", "r") as file:
        lines = file.readlines()
        config["username"] = lines[0].strip()
        config["password"] = lines[1].strip()

    with requests.Session() as session:
        session.auth = requests.auth.HTTPDigestAuth(config["username"], config["password"])
        response = requests.post(config["url_base"], auth=session.auth)
        print(response.text)

if __name__ == "__main__":
    sys.exit(main())
