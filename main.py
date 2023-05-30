import os
import pathlib
import sys

import robot_web_services
import speech_recognition
import visual_detection


def job(robot, speech, visual) -> int:
    print("Hello, World!")

    # // Optional
    # - [Greifen] Yumi bewegt Arm-1 und greift das Gummiteil
    # - Yumi bewegt Arm-1 und "pudert" das Gummiteil
    # - Yumi bewegt Arm-1 und legt das Gummiteil in den Verpresser
    # - Yumi bewegt Arm-1 zurück in die Startposition

    # // Must-Have
    # - [Greifen] Yumi bewegt Arm-1 und greift das Metallteil
    # - Yumi bewegt Arm-1 und legt das Metallteil in den Verpresser
    # - Yumi bewegt Arm-1 zurück in die Startposition

    # // Must-Have
    # - Yumi bewegt Arm-2 und hebt den Hebel hoch
    # - [Optional] Yumi bewegt Arm-2 und legt den Hebel um
    # - Yumi bewegt Arm-2 zurück in die Startposition

    # // Must-Have
    # - Yumi bewegt Arm-2 und legt das fertige Produkt in eine Box
    # - Yumi bewegt Arm-2 zurück in die Startposition


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
