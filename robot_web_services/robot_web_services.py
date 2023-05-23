import ast
import enum
import json
import math
import requests.auth
import requests
import time
import logging

# Address used to organize ET elements
namespace = '{http://www.w3.org/1999/xhtml}'

logger = logging.getLogger(__name__)


class ControllerStates(enum.Enum):
    init = "init"
    motoroff = "motoroff"
    motoron = "motoron"
    guardstop = "guardstop"
    emergencystop = "emergencystop"
    emergencystopreset = "emergencystopreset"
    sysfail = "sysfail"


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


class Robot:
    """
    Python Interface for ABB RobotWebServices (REST-API)\n
    Modified version of from GitHub project <mhiversflaten/ABB-Robot-Machine-Vision>\n
    Source: <https://github.com/mhiversflaten/ABB-Robot-Machine-Vision.git>
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded;v=2.0"
    }

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
            url=url,
            headers=self.headers,
            cookies=self.session.cookies,
            auth=self.session.auth
        )

        response = APIResponse(response)

        logger.debug(response.status_code)
        logger.debug(response.text)
        logger.debug(response.json)

        return response


    def _api_post(self, resource, payload = None, headers = None) -> APIResponse:
        url = f"{self.base_url}/{resource}"
        url = f"{url}&json=1" if "?" in url else f"{url}?json=1"

        headers = headers or self.headers

        repsonse = self.session.post(
            url=url,
            data=payload,
            headers=headers,
            cookies=self.session.cookies,
            auth=self.session.auth
        )

        response = APIResponse(repsonse)

        logger.debug(response.status_code)
        logger.debug(response.text)
        logger.debug(response.json)

        return response


    def login(self):
        self._api_post(
            resource="/users?action=set-locale",
            payload="type=local"
        )

    def rmmp(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;v=2.0"
        }

        self._api_post(
            resource="/users/rmmp",
            payload="privilege=modify",
            headers=headers
        )
    
    def get_system(self):
        self._api_get("/rw/system?json=1")


    def request_mastership(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;v=2.0"
        }

        self._api_post(
            resource="/rw/mastership?action=request",
            headers=headers
        )


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
        state = response.json["_embedded"]["_state"][0]['ctrlstate']
        state = ControllerStates[state]

        return state


    def set_controller_state(self, ctrl_state) -> APIResponse:
        payload = {"ctrl-state": ctrl_state}

        response = self._api_post("rw/panel/ctrlstate?action=setctrlstate", payload)

        print(response)

        if response.status_code != 204:
            raise Exception("Could not change controller state")

        return response


    def motors_on(self) -> None:
        """Turns the robot's motors on.
        Operation mode has to be AUTO.
        """

        self.set_controller_state(ControllerStates.motoron.value)


    def motors_off(self):
        """Turns the robot's motors off.
        """

        payload = {'ctrl-state': ControllerStates.motoroff}
        self._api_post("/rw/panel/ctrlstate?action=setctrlstate", payload)


class RobotArm():
    def __init__(self, robot: Robot, mechunit: str) -> None:
        self._robot = robot
        self._mechunit = mechunit


    def rotation_get(self):
        response = self._robot._api_get(f"/rw/motionsystem/mechunits/{self._mechunit}/jointtarget")

        axis_get_value = lambda response, axis : response.json["_embedded"]["_state"][0][f"rax_{axis}"]
        
        axis_values = [axis_get_value(response, axis) for axis in range(1, (6 + 1))]
        axis_values = [float(value) for value in axis_values]

        return axis_values

    
    def _arm_job(self, axis1, axis2, axis3, axis4, axis5, axis6, ccount=0, inc_mode="Small"):
        self._robot._api_post(f"/rw/motionsystem/{self._mechunit}")

        payload = f"axis1={axis1}&axis2={axis2}&axis3={axis3}&axis4={axis4}&axis5={axis5}&axis6={axis6}"
        payload = f"{payload}&ccount={ccount}&inc-mode={inc_mode}"

        self._robot._api_post(resource="/rw/motionsystem?action=jog", payload=payload,)


    def rotation_set(self, axis1, axis2, axis3, axis4, axis5, axis6):        
        axis_target = [axis1, axis2, axis3, axis4, axis5, axis6]
        axis_target = [int(value) for value in axis_target]

        evaluate = lambda target, value : (+1) if (value < target) else (-1) if (value > target) else (0)

        while True:
            axis_current = self.rotation_get()
            axis_current = [int(value) for value in axis_current]
            
            if (axis_target == axis_current): break

            movement = [evaluate(target, value) for target, value in zip(axis_target, axis_current)]
            self._arm_job(*movement, 0, "Large")
            
            time.sleep(1)
