import os
import pathlib
import sys
import logging
import time

import robot_web_services.robot_web_services as robot_web_services
import speech_recognition


def run_task_1(robot):
    position_home = [0, -130, 30, 0, 40, 0]

    # robot.arm_left.rotation_set(*position_home)
    robot.arm_right.rotation_set(*position_home)


def run_task_2(robot):
    robtarget = [[-9.578368507,-182.609892723,198.627808149],[0.066010726,-0.842420918,-0.111214912,-0.523068661],[0,0,0,4],[-135,9E+09,9E+09,9E+09,9E+09,9E+09]]
    position_target = robot_web_services.robtarget_to_position_target(robtarget)
    payload = robot_web_services.position_target_to_payload(position_target)

    robot._api_post("/rw/motionsystem?action=positiontarget", payload)


def run_task_3(robot):
    robot._api_post(f"/rw/motionsystem/ROB_1?action=set")
    robot._api_post(f"/rw/motionsystem?action=set", "ROB_1")
    robot._api_post(f"/rw/motionsystem?action=ROB_1")
    robot._api_post(f"/rw/motionsystem?action=ROB_1", "ROB_1")
    robot._api_post(f"/rw/motionsystem?action=ROB_1", "mechunit=ROB_1")

    robot._api_post(f"/rw/motionsystem/ROB_L?action=set")

    robot._api_post(f"/rw/motionsystem/ROB_1_L")
    robot._api_post(f"/rw/motionsystem/ROB_L?action=ROB_1")
    robot._api_post(f"/rw/motionsystem?action=set", "ROB_1_L")


def run_task_4(robot):
    jointtarget = [[60.66,-92.386666667,-17.68,-11.6,-0.613333333,45.8],[-119.073333333,9E+09,9E+09,9E+09,9E+09,9E+09]]
    position_custom = robot_web_services.jointtarget_to_array(jointtarget)

    # robot.arm_left.rotation_set(*position_custom)
    robot.arm_right.rotation_set(*position_custom)


def run_task(config):
    robot = robot_web_services.Robot(
        base_url=config["url_base"],
        username=config["username"],
        password=config["password"],
        model = config["model"]
    )

    robot.ready_robot()

    return run_task_1(robot)


def main() -> int:
    print("Hello, World!")

    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    config = {}

    with open(".secrets/api.key", "r") as file:
        lines = file.readlines()
        config["username"] = lines[0].strip()
        config["password"] = lines[1].strip()

    config["url_base"] = "http://localhost:80"
    config["model"] = "IRB14000"

    run_task(config)

    return 0


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
