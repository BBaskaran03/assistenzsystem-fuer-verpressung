import os
import pathlib
import sys

import robot_web_services
import speech_recognition


def main() -> int:
    print("Hello, World!")
    return 0


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
