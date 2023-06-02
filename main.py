import os
import pathlib
import sys

import robot_web_services
from robot_web_services.positions import Position
from robot_web_services.positions import Positions
import speech_recognition


positions = None


def main() -> int:
    global positions
    positions_file = "./positions.json"

    print("Hello, World!")

    positions = Positions.from_file(positions_file)
    positions["root"] = Position.from_worldpoint(0, 0, 0)
    positions.to_file(positions_file)

    return 0


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
