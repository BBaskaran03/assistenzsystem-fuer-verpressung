"""Robot Web Services"""

import enum
import json
import logging
import pathlib
import sys
import time

import requests
import requests.auth

logger = logging.getLogger(__name__)


class ControllerStates(enum.Enum):
    init = "init"
    motoroff = "motoroff"
    motoron = "motoron"
    guardstop = "guardstop"
    emergencystop = "emergencystop"
    emergencystopreset = "emergencystopreset"
    sysfail = "sysfail"


class RWSException(Exception):
    pass


class APIException(RWSException):
    def __init__(self, message, response):
        super().__init__(message)
        self.response = response


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


class RobotArm:
    def __init__(self, robot, mechunit: str) -> None:
        self._robot = robot
        self._mechunit = mechunit

    def rotation_get(self):
        response = self._robot._api_get(
            f"/rw/motionsystem/mechunits/{self._mechunit}/jointtarget"
        )

        axis_get_value = lambda response, axis: response.json["_embedded"]["_state"][0][
            f"rax_{axis}"
        ]

        axis_values = [axis_get_value(response, axis) for axis in range(1, (6 + 1))]
        axis_values = [float(value) for value in axis_values]

        return axis_values

    def _arm_job(
        self, axis1, axis2, axis3, axis4, axis5, axis6, ccount=0, inc_mode="Small"
    ):
        self._robot._api_post(f"/rw/motionsystem/{self._mechunit}") # TODO: Fix this

        payload = f"axis1={axis1}&axis2={axis2}&axis3={axis3}&axis4={axis4}&axis5={axis5}&axis6={axis6}"
        payload = f"{payload}&ccount={ccount}&inc-mode={inc_mode}"

        self._robot._api_post(resource="/rw/motionsystem?action=jog", payload=payload)

    def rotation_set(self, axis1, axis2, axis3, axis4, axis5, axis6):
        axis_target = [axis1, axis2, axis3, axis4, axis5, axis6]
        axis_target = [int(value) for value in axis_target]

        evaluate = (
            lambda target, value: (+1)
            if (value < target)
            else (-1)
            if (value > target)
            else (0)
        )

        while True:
            axis_current = self.rotation_get()
            axis_current = [int(value) for value in axis_current]

            if axis_target == axis_current:
                break

            movement = [
                evaluate(target, value)
                for target, value in zip(axis_target, axis_current)
            ]
            self._arm_job(*movement, 0, "Large")

            time.sleep(1)


class RobotWebServices:
    """
    Python Interface for ABB RobotWebServices (REST-API)\n
    Modified version of from GitHub project <mhiversflaten/ABB-Robot-Machine-Vision>\n
    Source: <https://github.com/mhiversflaten/ABB-Robot-Machine-Vision.git>
    """

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded;v=2.0",
    }

    def __init__(self, hostname: str, username: str, password: str, model: str):
        self.hostname = hostname

        self.model = model
        self._adapt_to_model()

        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPDigestAuth(username, password)

    def _adapt_to_model(self):
        if self.model == "IRB14000":
            self.arm_left = RobotArm(self, "ROB_L")
            self.arm_right = RobotArm(self, "ROB_R")
            return

        raise RWSException("Unknown model")

    def _handle_response(self, resource, response):
        # (200) HTTP_OK => Standard response for successful HTTP requests.
        if response.status_code == 200: pass

        # (201) CREATED => The request has been fulfilled, and a new resource is created
        if response.status_code == 201: pass

        # (202) ACCEPTED => The request has been accepted for processing, but the processing has not been completed
        if response.status_code == 202: pass

        # (204) NO_CONTENT => The request has been successfully processed, but is not returning any content
        if response.status_code == 204: pass

        # (301) MOVED_PERMANENTLY => The requested page has moved to a new URL
        if response.status_code == 301: pass

        # (304) NOT_MODIFIED => Indicates the requested page has not been modified since last requested
        if response.status_code == 304: pass

        # (400) BAD_REQUEST => The request cannot be fulfilled due to bad syntax
        if response.status_code == 400: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (401) UNAUTHORIZED => The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided
        if response.status_code == 401: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (403) FORBIDDEN => The request was a legal request, but the server is refusing to respond to it
        if response.status_code == 403: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (404) NOT_FOUND => The requested page could not be found but may be available again in the future
        if response.status_code == 404: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (405) METHOD_NOT_ALLOWED => A request was made of a page using a request method not supported by that page
        if response.status_code == 405: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (406) NOT_ACCEPTABLE => The server can only generate a response that is not accepted by the client
        if response.status_code == 406: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (409) CONFLICT => The request could not be completed due to a conflict with the current state of the target resource
        if response.status_code == 409: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (410) GONE => The requested page is no longer available
        if response.status_code == 410: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (415) UNSUPPORTED_MEDIA => The server will not accept the request, because the media type is not supported
        if response.status_code == 415: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (500) INTERNAL_SERVER_ERROR => A generic error message, given when no more specific message is suitable
        if response.status_code == 500: raise APIException(f"[ERROR] {response.status_code} | {response.text}", response)

        # (501) NOT_IMPLEMENTED => The server either does not recognize the request method, or it lacks the ability to fulfill the request
        if response.status_code == 501: pass

        # (503) SERVICE_UNAVAILABLE => The server is currently unavailable (overloaded or down)
        if response.status_code == 503: pass

    def _api_get(self, resource) -> APIResponse:
        url = f"{self.hostname}/{resource}"
        url = f"{url}&json=1" if "?" in url else f"{url}?json=1"

        response = self.session.get(
            url=url,
            headers=self.headers,
            cookies=self.session.cookies,
            auth=self.session.auth,
        )

        response = APIResponse(response)
        self._handle_response(resource, response)

        return response

    def _api_post(self, resource, payload=None) -> APIResponse:
        url = f"{self.hostname}/{resource}"
        url = f"{url}&json=1" if "?" in url else f"{url}?json=1"

        response = self.session.post(
            url=url,
            data=payload,
            headers=self.headers,
            cookies=self.session.cookies,
            auth=self.session.auth,
        )

        response = APIResponse(response)
        self._handle_response(resource, response)

        return response

    def login(self):
        self._api_post(resource="/users?action=set-locale", payload="type=local")

    def rmmp(self):
        self._api_post(resource="/users/rmmp", payload="privilege=modify")

    def get_system(self):
        self._api_get("/rw/system?json=1")

    def request_mastership(self):
        self._api_post(resource="/rw/mastership?action=request")

    def release_mastership(self):
        self._api_post("/rw/mastership?action=release")

    def ready_robot(self):
        self.login()

        time.sleep(5)

        self.rmmp()
        self.request_mastership()

    def get_controller_state(self) -> ControllerStates:
        """
        Get the controller state.
        RAPID can only be executed and the robot can only be moved in the `motoron` state.

        :returns: The controller state
        :rtype: ControllerStates
        """

        response = self._api_get("rw/panel/ctrlstate")
        state = response.json["_embedded"]["_state"][0]["ctrlstate"]
        state = ControllerStates[state]

        return state

    def set_controller_state(self, ctrl_state) -> APIResponse:
        payload = {"ctrl-state": ctrl_state}

        response = self._api_post("rw/panel/ctrlstate?action=setctrlstate", payload)

        print(response)

        if response.status_code != 204:
            raise APIException("Could not change controller state", response)

        return response

    def motors_on(self) -> None:
        """Turns the robot's motors on.
        Operation mode has to be AUTO.
        """

        self.set_controller_state(ControllerStates.motoron.value)

    def motors_off(self):
        """Turns the robot's motors off."""

        payload = {"ctrl-state": ControllerStates.motoroff}
        self._api_post("/rw/panel/ctrlstate?action=setctrlstate", payload)


def main() -> int:
    print("Hello, World")

    config_file = pathlib.Path("./config.json")

    if config_file.exists() == False:
        logger.critical("Config file is missing")
        raise Exception("Configuration file not found")

    with open(config_file, "r", encoding="utf-8") as config_file:
        logger.log("Loading config from file")
        config = json.load(config_file)

    robot = RobotWebServices(
        hostname=config["Robot Web Services"]["hostname"],
        username=config["Robot Web Services"]["username"],
        password=config["Robot Web Services"]["password"],
        model=config["Robot Web Services"]["model"]
    )

    position_home = [0, -130, 30, 0, 40, 0]

    # robot.arm_left.rotation_set(*position_home)
    robot.arm_right.rotation_set(*position_home)

    return 0


if __name__ == "__main__":
    sys.exit(main())
