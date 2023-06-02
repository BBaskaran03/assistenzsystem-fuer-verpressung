#!/usr/bin/env python

import os
import pathlib
import time
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

    robot = robot_web_services.Robot(
        base_url=config["url_base"],
        username=config["username"],
        password=config["password"],
    )

    robot.task_1()
    time.sleep(5)
    robot.task_2()
    robot.task_3()

    # position_1 = [91, 5, -5, 5, -5, 10]
    # robot.arm_right_rotate_to(*position_1)

    # robot.arm_right_rotate_to(axis1=90,axis2=0,axis3=0,axis4=0,axis5=0,axis6=0)
    robot.arm_right_rotate_to(axis1=91,axis2=5,axis3=-5,axis4=5,axis5=-5,axis6=10)

    # print(robot._api_get(resource="/rw/motionsystem/mechunits/ROB_L/jointtarget"))
    
# [[-9.578368507,182.609892723,198.627808149],[0.066010726,0.842420918,-0.111214912,0.523068661],[0,0,0,4],[135,9E+09,9E+09,9E+09,9E+09,9E+09]]
# [[0,-130,30,0,40,0],[135,9E+09,9E+09,9E+09,9E+09,9E+09]]

    # Get winkel von arm links
    # print(robot._api_get(resource="/rw/motionsystem/mechunits/ROB_L/jointtarget"))

    # robot.task_1()
    # import time
    # time.sleep(5)
    # robot.task_2()
    # robot.task_3()
    # robot.task_4()

    # for index in range(100):
    #     robot.move_arm_right(axis1=1,axis2=0,axis3=0,axis4=0,axis5=0,axis6=0,ccount=0,inc_mode="Large")
    #     time.sleep(1)


    # print(robot._api_get(resource="/rw/motionsystem/mechunits/ROB_L/axes/1?resource=axis-pose"))
    # print(robot._api_get(resource="/rw/motionsystem/mechunits"))

    # 90
    # robot.move_arm_right(axis1=1,axis2=0,axis3=0,axis4=0,axis5=0,axis6=0,ccount=0,inc_mode="Large")
    # # 90,14
    
    # time.sleep(5)

    # # 90,14
    # robot.move_arm_right(axis1=-1,axis2=0,axis3=0,axis4=0,axis5=0,axis6=0,ccount=0,inc_mode="Large")
    # 98,86

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
