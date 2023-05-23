import os
import pathlib
import sys
import logging
import time

import robot_web_services.robot_web_services as robot_web_services
import speech_recognition


def process(config):
    robot = robot_web_services.Robot(
        base_url=config["url_base"],
        username=config["username"],
        password=config["password"],
    )

    robot.ready_robot()

    position_1 = [91, 5, -5, 5, -5, 10]
    robot.arm_right_rotate_to(*position_1)


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

    process(config)

    return 0


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
