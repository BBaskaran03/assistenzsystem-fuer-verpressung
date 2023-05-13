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

    irb14000 = robot_web_services.RobotWebServices(
        base_url=config["url_base"],
        username=config["username"],
        password=config["password"],
    )

    # irb14000.get_system()

    irb14000.request_mastership()

    print(irb14000._api_post(
        "/rw/motionsystem?action=jog",
        value="axis1=900&axis2=0&axis3=0&axis4=0&axis5=0&axis6=0&ccount=0&inc-mode=Large"
    ))

    # # print(irb14000.get_controller_state())
    # # irb14000.motors_off()
    # # print(irb14000.get_controller_state())

    # print(f"\n{'-' * 100}\n")

    # # print(irb14000.get_controller_state())
    # irb14000.motors_on()
    # print(irb14000.get_controller_state())

    # irb14000.release_mastership()

    # print(irb14000._api_get("/rw/motionsystem/mechunits"))
    # print(irb14000.api_get_pretty("/rw/motionsystem/mechunits/ROB_R"))
    # print(irb14000.api_get_pretty("/rw/motionsystem/mechunits/ROB_R/axes"))
    # print(irb14000.api_get_pretty("/rw/motionsystem/mechunits/ROB_R/axes/1"))
    # print(irb14000.api_get_pretty("/rw/motionsystem/mechunits/ROB_R/axes/1?resource=axis-pose"))

    # print(irb14000.api_post_pretty(
    #     "/rw/motionsystem/mechunits/ROB_R/axes/1?resource=axis-pose",
    #     "axis-pose",
    #     "x=0&y=0&z=0&q1=2&q2=0&q3=0&q4=0"
    # ))

if __name__ == "__main__":
    sys.exit(main())
