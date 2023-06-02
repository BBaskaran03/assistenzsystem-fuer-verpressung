import sys
import pathlib
import ast
import enum
import json
import math
import requests.auth
import requests
import time
import logging


logger = logging.getLogger(__name__)


def robtarget_to_position_target(robtarget) -> dict():
    position_target = {}

    position_target["pos-x"]=robtarget[0][(1-1)]
    position_target["pos-y"]=robtarget[0][(2-1)]
    position_target["pos-z"]=robtarget[0][(3-1)]
    position_target["orient-q1"]=robtarget[1][(1-1)]
    position_target["orient-q2"]=robtarget[1][(2-1)]
    position_target["orient-q3"]=robtarget[1][(3-1)]
    position_target["orient-q4"]=robtarget[1][(4-1)]
    position_target["config-j1"]=robtarget[2][(1-1)]
    position_target["config-j4"]=robtarget[2][(2-1)]
    position_target["config-j6"]=robtarget[2][(3-1)]
    position_target["config-jx"]=robtarget[2][(4-1)]
    position_target["extjoint-1"]=robtarget[3][(1-1)]
    position_target["extjoint-2"]=robtarget[3][(2-1)]
    position_target["extjoint-3"]=robtarget[3][(3-1)]
    position_target["extjoint-4"]=robtarget[3][(4-1)]
    position_target["extjoint-5"]=robtarget[3][(5-1)]
    position_target["extjoint-6"]=robtarget[3][(6-1)]

    return position_target


def position_target_to_payload(position_target):
    payload = ""

    payload = f'{payload}pos-x={position_target["pos-x"]}&'
    payload = f'{payload}pos-y={position_target["pos-y"]}&'
    payload = f'{payload}pos-z={position_target["pos-z"]}&'
    payload = f'{payload}orient-q1={position_target["orient-q1"]}&'
    payload = f'{payload}orient-q2={position_target["orient-q2"]}&'
    payload = f'{payload}orient-q3={position_target["orient-q3"]}&'
    payload = f'{payload}orient-q4={position_target["orient-q4"]}&'
    payload = f'{payload}config-j1={position_target["config-j1"]}&'
    payload = f'{payload}config-j4={position_target["config-j4"]}&'
    payload = f'{payload}config-j6={position_target["config-j6"]}&'
    payload = f'{payload}config-jx={position_target["config-jx"]}&'
    payload = f'{payload}extjoint-1={position_target["extjoint-1"]}&'
    payload = f'{payload}extjoint-2={position_target["extjoint-2"]}&'
    payload = f'{payload}extjoint-3={position_target["extjoint-3"]}&'
    payload = f'{payload}extjoint-4={position_target["extjoint-4"]}&'
    payload = f'{payload}extjoint-5={position_target["extjoint-5"]}&'
    payload = f'{payload}extjoint-6={position_target["extjoint-6"]}&'

    payload = payload[:-1]

    return payload


def jointtarget_to_array(jointtarget):
    axis1=jointtarget[0][(1-1)]
    axis2=jointtarget[0][(2-1)]
    axis3=jointtarget[0][(3-1)]
    axis4=jointtarget[0][(4-1)]
    axis5=jointtarget[0][(5-1)]
    axis6=jointtarget[0][(6-1)]

    return [axis1, axis2, axis3, axis4, axis5, axis6]


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


class RobotArm():
    def __init__(self, robot, mechunit: str) -> None:
        self._robot = robot
        self._mechunit = mechunit


    def rotation_get(self):
        response = self._robot._api_get(f"/rw/motionsystem/mechunits/{self._mechunit}/jointtarget")

        axis_get_value = lambda response, axis : response.json["_embedded"]["_state"][0][f"rax_{axis}"]
        
        axis_values = [axis_get_value(response, axis) for axis in range(1, (6 + 1))]
        axis_values = [float(value) for value in axis_values]

        return axis_values

    
    def _arm_job(self, axis1, axis2, axis3, axis4, axis5, axis6, ccount=0, inc_mode="Small"):
        self._robot._api_post(f"/rw/motionsystem/{self._mechunit}") # TODO: Fix this

        payload = f"axis1={axis1}&axis2={axis2}&axis3={axis3}&axis4={axis4}&axis5={axis5}&axis6={axis6}"
        payload = f"{payload}&ccount={ccount}&inc-mode={inc_mode}"

        self._robot._api_post(resource="/rw/motionsystem?action=jog", payload=payload)


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


class RobotWebServices:
    """
    Python Interface for ABB RobotWebServices (REST-API)\n
    Modified version of from GitHub project <mhiversflaten/ABB-Robot-Machine-Vision>\n
    Source: <https://github.com/mhiversflaten/ABB-Robot-Machine-Vision.git>
    """

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded;v=2.0"
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
        
        raise Exception("Unknown model")


    def _api_get(self, resource) -> APIResponse:
        url = f"{self.hostname}/{resource}"
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


    def _api_post(self, resource, payload = None) -> APIResponse:
        url = f"{self.hostname}/{resource}"
        url = f"{url}&json=1" if "?" in url else f"{url}?json=1"

        repsonse = self.session.post(
            url=url,
            data=payload,
            headers=self.headers,
            cookies=self.session.cookies,
            auth=self.session.auth
        )

        response = APIResponse(repsonse)

        logger.debug(response.status_code)
        logger.debug(response.text)
        logger.debug(response.json)

        return response


    def login(self):
        self._api_post(resource="/users?action=set-locale", payload="type=local")

    def rmmp(self):
        self._api_post(resource="/users/rmmp",payload="privilege=modify")


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
        base_url=config["Robot Web Services"]["hostname"],
        username=config["Robot Web Services"]["username"],
        password=config["Robot Web Services"]["password"],
    )

    position_home = [0, -130, 30, 0, 40, 0]

    # robot.arm_left.rotation_set(*position_home)
    robot.arm_right.rotation_set(*position_home)

    return 0


if __name__ == "__main__":
    sys.exit(main())
