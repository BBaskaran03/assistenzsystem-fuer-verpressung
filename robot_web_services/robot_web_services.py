"""Robot Web Services"""

import enum
import json
import logging
import pathlib
import sys
import time

import requests
import requests.auth

from robot_web_services.positions import Position, Positions, Robtarget

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
    def __init__(self, resource: str, response: requests.Response):
        self._resource = resource
        self._response = response

        logging.debug(f"{resource} | {response.status_code} | {response.text}")

    def _maybe_json(self) -> dict:
        try:
            return json.loads(self._response.text)
        except json.decoder.JSONDecodeError:
            return None

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def text(self) -> str:
        return self._response.text

    @property
    def json(self) -> json:
        return self._maybe_json()

    def __repr__(self) -> str:
        return json.dumps(self.json, indent=4)

    def check(self):
        status_okay = ["200", "201", "202", "204", "301", "304"]
        status_bad = [
            "400",
            "401",
            "403",
            "404",
            "405",
            "406",
            "409",
            "410",
            "415",
            "500",
            "501",
            "503",
        ]

        if self.status_code in status_okay:
            return

        if self.status_code in status_bad:
            message = f"[ERROR] {self.status_code} | {self._resource} | {self.text}"
            raise APIException(message, self._response)


class API:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded;v=2.0",
    }

    def __init__(self, hostname: str, username: str, password: str):
        self.hostname = hostname
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPDigestAuth(username, password)

    def get(self, resource) -> APIResponse:
        url = f"{self.hostname}{resource}"
        url = f"{url}&json=1" if "?" in url else f"{url}?json=1"

        response = self.session.get(
            url=url,
            headers=self.headers,
            cookies=self.session.cookies,
            auth=self.session.auth,
        )

        response = APIResponse(resource, response)
        response.check()

        return response

    def post(self, resource, payload=None) -> APIResponse:
        url = f"{self.hostname}{resource}"
        url = f"{url}&json=1" if "?" in url else f"{url}?json=1"

        response = self.session.post(
            url=url,
            data=payload,
            headers=self.headers,
            cookies=self.session.cookies,
            auth=self.session.auth,
        )

        response = APIResponse(resource, response)
        response.check()

        return response


class RobotArm:
    def __init__(self, robot, mechunit: str, api: API, home: Position) -> None:
        self._robot = robot
        self._mechunit = mechunit
        self._api = api
        self.home = home

    @property
    def name(self) -> str:
        return self._mechunit

    def _rotation_get(self):
        response = self._api.get(
            f"/rw/motionsystem/mechunits/{self._mechunit}/jointtarget"
        )

        axis_get_value = lambda response, axis: response.json["_embedded"]["_state"][0][
            f"rax_{axis}"
        ]

        axis_values = [axis_get_value(response, axis) for axis in range(1, (6 + 1))]
        axis_values = [float(value) for value in axis_values]

        return axis_values

    @property
    def rotation(self):
        return self._rotation_get()

    def _arm_jog(
        self, axis1, axis2, axis3, axis4, axis5, axis6, ccount=0, inc_mode="Small"
    ):
        self._api.post(f"/rw/motionsystem/{self._mechunit}")  # TODO: Fix this

        payload = f"axis1={axis1}&axis2={axis2}&axis3={axis3}&axis4={axis4}&axis5={axis5}&axis6={axis6}"
        payload = f"{payload}&ccount={ccount}&inc-mode={inc_mode}"

        self._api.post(resource="/rw/motionsystem?action=jog", payload=payload)

    def _rotation_set(self, axis1, axis2, axis3, axis4, axis5, axis6):
        axis_target = [axis1, axis2, axis3, axis4, axis5, axis6]
        axis_target = [int(value) for value in axis_target]

        logger.info("Moving to rotation <{axis_target}>")

        def evaluate(target, value):
            if value < target:
                return +1
            if value > target:
                return -1
            return 0

        while True:
            axis_current = [int(value) for value in self.rotation]

            if axis_target == axis_current:
                break

            movement = [
                evaluate(target, value)
                for target, value in zip(axis_target, axis_current)
            ]
            self._arm_jog(*movement, 0, "Large")

            time.sleep(1)

    def rotate_to(self, axis1, axis2, axis3, axis4, axis5, axis6):
        return self._rotation_set(axis1, axis2, axis3, axis4, axis5, axis6)

    def rapid_variable_get(self, variable):
        """Gets the raw value of any RAPID variable."""

        resource = (
            f"/rw/rapid/symbol/data/RAPID/T_{self._mechunit}/{variable};value?json=1"
        )
        response = self._api.get(resource)
        value = response.json["_embedded"]["_state"][0]["value"]

        return value

    @property
    def robtarget(self):
        # def robtarget(self) -> Robtarget:
        response = self._api.get(
            f"/rw/rapid/tasks/T_{self._mechunit}/motion?resource=robtarget"
        )
        output = response.json["_embedded"]["_state"][0]

        # Convert output from json to list
        robtarget = [
            [output["x"], output["y"], output["z"]],
            [output["q1"], output["q2"], output["q3"], output["q4"]],
            [output["cf1"], output["cf4"], output["cf6"], output["cfx"]],
            [
                output["ej1"],
                output["ej2"],
                output["ej3"],
                output["ej4"],
                output["ej5"],
                output["ej6"],
            ],
        ]

        # Convert values from string to float
        for key, value in enumerate(robtarget):
            robtarget[key] = [float(value) for value in value]

        # Create robtarget
        robtarget = Robtarget(robtarget)

        return robtarget

    def rapid_variable_set(self, variable, value):
        """Sets the value of any RAPID variable.
        Unless the variable is of type 'num', 'value' has to be a string.
        """

        resource = (
            f"/rw/rapid/symbol/data/RAPID/T_{self._mechunit}/{variable}?action=set"
        )

        self._api.post(resource, payload={"value": str(value)})

    def gripper_open(self):
        logging.debug("Gripper will open")

        # self._robot.rapid_start()
        self.rapid_variable_set("ready", "TRUE")
        self.rapid_variable_set("job", "2")

        time.sleep(2)

        self.rapid_variable_set("ready", "FALSE")
        self.rapid_variable_set("job", "0")
        # self._robot.rapid_stop()

        logging.debug("Gripper has been opened")

    def gripper_close(self):
        logging.debug("Gripper will close")

        # self._robot.rapid_start()
        self.rapid_variable_set("ready", "TRUE")
        self.rapid_variable_set("job", "3")

        time.sleep(2)

        self.rapid_variable_set("ready", "FALSE")
        self.rapid_variable_set("job", "0")
        # self._robot.rapid_stop()

        logging.debug("Gripper has been closed")

    def move_to(self, position: Position):
        def compare(robt1: Position, robt2: Position):
            robt1 = [
                round(float(robt1.x), 2),
                round(float(robt1.y), 2),
                round(float(robt1.z), 2),
            ]
            robt2 = [
                round(float(robt2.x), 2),
                round(float(robt2.y), 2),
                round(float(robt2.z), 2),
            ]

            logger.debug(f"Comparing position <{robt1}> with <{robt2}>")
            return robt1 == robt2

        if compare(self.robtarget, position):
            return

        # self._robot.rapid_start()

        self.rapid_variable_set("job", "1")

        self.rapid_variable_set("target", position.to_rapid_robtarget())
        logger.debug(f"Moving to target <{position}>")
        self.rapid_variable_set("ready", "TRUE")

        while compare(self.robtarget, position) == False:
            time.sleep(1)

        logger.debug("Stopping movement")
        self.rapid_variable_set("ready", "FALSE")
        self.rapid_variable_set("job", "0")
        # self._robot.rapid_stop()
        time.sleep(1)

    def move_to_home(self):
        self.move_to(self.home)

    def grab(self, position: Position):
        # TODO: Implement this
        pass

    def drop(self):
        # TODO: Implement this
        pass


class RobotWebServices:
    """
    Python Interface for ABB RobotWebServices (REST-API)\n
    Modified version of from GitHub project <mhiversflaten/ABB-Robot-Machine-Vision>\n
    Source: <https://github.com/mhiversflaten/ABB-Robot-Machine-Vision.git>
    """

    def __init__(self, hostname: str, username: str, password: str, model: str):
        self._api = API(hostname, username, password)

        self.arms = {}
        self.model = model
        self._adapt_to_model()

    def _adapt_to_model(self):
        if self.model == "IRB14000":
            arm_left_home = [
                [-9.578368507, 182.609892723, 198.627808149],
                [0.066010726, 0.842420918, -0.111214912, 0.523068661],
                [0, 0, 0, 4],
                [135, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
            self.arms["arm_left"] = RobotArm(
                self, "ROB_L", self._api, Position.from_robtarget(arm_left_home)
            )
            self.arm_left = self.arms["arm_left"]

            arm_right_home = [
                [-9.578368507, -182.609892723, 198.627808149],
                [0.066010726, -0.842420918, -0.111214912, -0.523068661],
                [0, 0, 0, 4],
                [-135, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
            self.arms["arm_right"] = RobotArm(
                self, "ROB_R", self._api, Position.from_robtarget(arm_right_home)
            )
            self.arm_right = self.arms["arm_right"]

            return

        raise RWSException("Unknown model")

    def login(self):
        self._api.post(resource="/users?action=set-locale", payload="type=local")

    def rmmp(self):
        self._api.post(resource="/users/rmmp", payload="privilege=modify")

    def get_system(self):
        self._api.get("/rw/system?json=1")

    def request_mastership(self):
        self._api.post(resource="/rw/mastership?action=request")

    def release_mastership(self):
        self._api.post("/rw/mastership?action=release")

    def ready_robot(self):
        self.rapid_stop()
        self.rapid_start()

        for arm in self.arms.values():
            arm.move_to_home()

    def get_controller_state(self) -> ControllerStates:
        """
        Get the controller state.
        RAPID can only be executed and the robot can only be moved in the `motoron` state.

        :returns: The controller state
        :rtype: ControllerStates
        """

        response = self._api.get("/rw/panel/ctrlstate")
        state = response.json["_embedded"]["_state"][0]["ctrlstate"]
        state = ControllerStates[state]

        return state

    def set_controller_state(self, ctrl_state) -> APIResponse:
        payload = {"ctrl-state": ctrl_state}

        response = self._api.post("/rw/panel/ctrlstate?action=setctrlstate", payload)

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
        self._api.post("/rw/panel/ctrlstate?action=setctrlstate", payload)

    def rapid_reset_pp(self):
        """Resets the program pointer to main procedure in RAPID."""

        response = self._api.post("/rw/rapid/execution?action=resetpp")

        if response.status_code != 204:
            logger.warning("Could not reset program pointer to main")
            raise APIException("[ERROR] rapid_reset_pp()", response)

        logger.debug("Program pointer reset to main")

    def rapid_start(self):
        """Resets program pointer to main procedure in RAPID and starts RAPID execution."""

        self.rapid_reset_pp()

        payload = {
            "regain": "continue",
            "execmode": "continue",
            "cycle": "once",
            "condition": "none",
            "stopatbp": "disabled",
            "alltaskbytsp": "false",
        }

        response = self._api.post("/rw/rapid/execution?action=start", payload)

        if response.status_code != 204:
            raise APIException("[ERROR] rapid_start()", response)

        logger.debug("RAPID execution started from main")

    def rapid_stop(self):
        """Stops RAPID execution."""

        payload = {"stopmode": "stop", "usetsp": "normal"}

        response = self._api.post("/rw/rapid/execution?action=stop", payload)

        if response.status_code != 204:
            logger.warning("Could not stop RAPID execution")
            raise APIException("[ERROR] rapid_stop()", response)

        logger.debug("RAPID execution stopped")


def main() -> int:
    print("Hello, World")

    config_file = pathlib.Path("./config.json")

    if config_file.exists() == False:
        logger.critical("Config file is missing")
        raise Exception("Configuration file not found")

    with open(config_file, "r", encoding="utf-8") as config_file:
        logger.debug("Loading config from file")
        config = json.load(config_file)

    robot = RobotWebServices(
        hostname=config["Robot Web Services"]["hostname"],
        username=config["Robot Web Services"]["username"],
        password=config["Robot Web Services"]["password"],
        model=config["Robot Web Services"]["model"],
    )

    # region positions
    positions = Positions()

    positions["home"] = Position.from_rotation([0, -130, 30, 0, 40, 0])
    # endregion positions

    def task_1():
        robot.ready_robot()
        # robot.arm_left.rotate_to(*list(positions["home"].rotation.to_array()))
        robot.arm_right.rotate_to(*list(positions["home"].rotation.to_array()))

    def task_2():
        robot.rapid_start()

        left_ready = robot.arm_left.rapid_variable_get("ready")
        print(left_ready)
        left_target = robot.arm_left.rapid_variable_get("target")
        print(left_target)

        right_ready = robot.arm_right.rapid_variable_get("ready")
        print(right_ready)
        right_target = robot.arm_right.rapid_variable_get("target")
        print(right_target)

        robot.rapid_stop()

    def task_3():
        def convert_position(position: Position) -> str:
            conversion = position.to_array()
            conversion[3][1::] = ["9E+09", "9E+09", "9E+09", "9E+09", "9E+09"]
            conversion = str(conversion).replace(" ", "")
            conversion = str(conversion).replace("'", "")

            return conversion

        def move_arm(robot: RobotWebServices, arm: RobotArm, target: Position):
            robot.rapid_start()

            target = convert_position(target)
            arm.rapid_variable_set("target", target)
            logging.debug(f"Moving to target <{target}>")
            arm.rapid_variable_set("ready", "TRUE")
            time.sleep(5)

            logging.debug("Stopping movement")
            arm.rapid_variable_set("ready", "FALSE")
            robot.rapid_stop()
            time.sleep(3)

        arm_left_position_1 = Position.from_robtarget(
            [
                [50, 210.610123632, 180.627879465],
                [0.066010741, 0.842421005, -0.11121506, 0.523068488],
                [0, 0, 0, 4],
                [141.502558998, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
        )
        arm_left_position_2 = Position.from_robtarget(
            [
                [60, 210.610123632, 180.627879465],
                [0.066010741, 0.842421005, -0.11121506, 0.523068488],
                [0, 0, 0, 4],
                [141.502558998, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
        )

        arm_right_position_1 = Position.from_robtarget(
            [
                [-9.578368507, -182.609892723, 198.627808149],
                [0.066010726, -0.842420918, -0.111214912, -0.523068661],
                [0, 0, 0, 4],
                [-135, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
        )
        arm_right_position_2 = Position.from_robtarget(
            [
                [-19.578368507, -182.609892723, 198.627808149],
                [0.066010726, -0.842420918, -0.111214912, -0.523068661],
                [0, 0, 0, 4],
                [-135, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
        )

        move_arm(robot, robot.arm_left, arm_left_position_1)
        move_arm(robot, robot.arm_left, arm_left_position_2)

        move_arm(robot, robot.arm_right, arm_right_position_1)
        move_arm(robot, robot.arm_right, arm_right_position_2)

    def task_4():
        arm_left_position_1 = Position.from_robtarget(
            [
                [50, 210.610123632, 180.627879465],
                [0.066010741, 0.842421005, -0.11121506, 0.523068488],
                [0, 0, 0, 4],
                [141.502558998, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
        )
        arm_left_position_2 = Position.from_robtarget(
            [
                [60, 210.610123632, 180.627879465],
                [0.066010741, 0.842421005, -0.11121506, 0.523068488],
                [0, 0, 0, 4],
                [141.502558998, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
        )

        arm_right_position_1 = Position.from_robtarget(
            [
                [-9.578368507, -182.609892723, 198.627808149],
                [0.066010726, -0.842420918, -0.111214912, -0.523068661],
                [0, 0, 0, 4],
                [-135, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
        )
        arm_right_position_2 = Position.from_robtarget(
            [
                [-19.578368507, -182.609892723, 198.627808149],
                [0.066010726, -0.842420918, -0.111214912, -0.523068661],
                [0, 0, 0, 4],
                [-135, 9e09, 9e09, 9e09, 9e09, 9e09],
            ]
        )

        robot.arm_left.move_to(arm_left_position_1)
        robot.arm_left.move_to(arm_left_position_2)

        robot.arm_right.move_to(arm_right_position_1)
        robot.arm_right.move_to(arm_right_position_2)

    task_4()

    return 0


if __name__ == "__main__":
    sys.exit(main())
