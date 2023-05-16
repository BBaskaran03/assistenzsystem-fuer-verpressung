#!/usr/bin/env python

import os
import pathlib
import sys
import logging

import robot_web_services


def main() -> int:
    file = pathlib.Path(__file__)
    os.chdir(file.parent)

    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    config = {}

    config["url_base"] = "http://localhost:80"

    with open(".secrets/api.key", "r") as file:
        lines = file.readlines()
        config["username"] = lines[0].strip()
        config["password"] = lines[1].strip()

    robot = robot_web_services.RobotWebServices(
        base_url=config["url_base"],
        username=config["username"],
        password=config["password"],
    )


    robot.task_1()
    import time
    time.sleep(5)
    robot.task_2()
    robot.task_3()
    robot.task_4()


    # robot.get_system()

    # robot.request_mastership()

    # print(robot._api_post(
    #     "/rw/motionsystem?action=jog",
    #     value="axis1=900&axis2=0&axis3=0&axis4=0&axis5=0&axis6=0&ccount=0&inc-mode=Large"
    # ))

    # # print(robot.get_controller_state())
    # # robot.motors_off()
    # # print(robot.get_controller_state())

    # print(f"\n{'-' * 100}\n")

    # # print(robot.get_controller_state())
    # robot.motors_on()
    # print(robot.get_controller_state())

    # robot.release_mastership()

    # print(robot._api_get("/rw/motionsystem/mechunits"))
    # print(robot.api_get_pretty("/rw/motionsystem/mechunits/ROB_R"))
    # print(robot.api_get_pretty("/rw/motionsystem/mechunits/ROB_R/axes"))
    # print(robot.api_get_pretty("/rw/motionsystem/mechunits/ROB_R/axes/1"))
    # print(robot._api_get("/rw/motionsystem/mechunits/ROB_R/axes/1?resource=axis-pose"))

    # print(robot.api_post_pretty(
    #     "/rw/motionsystem/mechunits/ROB_R/axes/1?resource=axis-pose",
    #     "axis-pose",
    #     "x=0&y=0&z=0&q1=2&q2=0&q3=0&q4=0"
    # ))

if __name__ == "__main__":
    sys.exit(main())
