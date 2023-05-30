import os
import pathlib
import sys

import robot_web_services
import speech_recognition
import visual_detection


def job(robot, speech, visual) -> int:
    print("Hello, World!")


def main() -> int:
    running = True

    robot = robot_web_services.Robot()
    speech = speech_recognition.Speech()
    visual = visual_detection.Dectector()

    return job(robot, speech, visual)


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
