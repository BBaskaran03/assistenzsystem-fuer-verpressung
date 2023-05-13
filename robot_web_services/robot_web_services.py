import ast
import json
import math
import requests.auth
import requests
import time


# Address used to organize ET elements
namespace = '{http://www.w3.org/1999/xhtml}'

logger = logging.getLogger(__name__)


class APIResponse:
    def __init__(self, response: requests.Response):
        self._status_code = response.status_code
        self._text = response.text
        self._json = self._maybe_json(response)


    def _maybe_json(self, response: requests.Response) -> json:
        try:
            return json.loads(response.text)
        except json.decoder.JSONDecodeError:
            return None


    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def text(self) -> str:
        return self._text

    @property
    def json(self) -> json:
        return self._json

    def __repr__(self) -> str:
        return json.dumps(self._json, indent=4)


class RobotWebServices:
    """
    Python Interface for ABB RobotWebServices (REST-API)\n
    Modified version of from GitHub project <mhiversflaten/ABB-Robot-Machine-Vision>\n
    Source: <https://github.com/mhiversflaten/ABB-Robot-Machine-Vision.git>
    """

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password

        self.session = requests.Session()
        self._authenticate()


    def _authenticate(self):
        self.session.auth = requests.auth.HTTPDigestAuth(self.username, self.password)


    def _api_get(self, resource) -> APIResponse:
        url = f"{self.base_url}/{resource}"
        url = f"{url}&json=1" if "?" in url else f"{url}?json=1"

        response = self.session.get(
            url,
            auth=self.session.auth,
            cookies=self.session.cookies
        )

        response = APIResponse(response)

        logger.debug(response.status_code)
        logger.debug(response.text)
        logger.debug(response.json)

        return response


    def _api_post(self, resource, value = None) -> APIResponse:
        url = f"{self.base_url}/{resource}"
        url = f"{url}&json=1" if "?" in url else f"{url}?json=1"

        payload = {"value": value}

        repsonse = self.session.post(
            url,
            data=payload,
            auth=self.session.auth,
            cookies=self.session.cookies
        )

        response = APIResponse(repsonse)

        logger.debug(response.status_code)
        logger.debug(response.text)
        logger.debug(response.json)

        return response


    def api_get(self, resource) -> json:
        response = self._api_get(resource)
        response_json = json.loads(response.text)

        return response_json


    def api_post(self, resource, value) -> json:
        response = self._api_post(resource, value)
        response_json = json.loads(response.text)

        return response_json

        return response_json_pretty
