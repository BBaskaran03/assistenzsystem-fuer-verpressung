import os
import pathlib
import threading
import sys

import robot_web_services
from robot_web_services.positions import Position
from robot_web_services.positions import Positions
import speech_recognition
import visual_detection


positions = None


def job_grab_and_place_rubber(robot, speech, visual):
    # - Yumi bewegt Arm-1 und greift das Gummiteil
    # - Yumi bewegt Arm-1 und "pudert" das Gummiteil
    # - Yumi bewegt Arm-1 und legt das Gummiteil in den Verpresser
    # - Yumi bewegt Arm-1 zurück in die Startposition

    speech.print("Ich greife jetzt das Gummiteil")
    
    robot.arm_left.move_to(positions["box_rubber"])

    position_rubber = visual.get_rubber()
    robot.arm_left.grab(position_rubber)

    robot.arm_left.move_to(positions["tool_rubber"])
    robot.arm_left.drop()

    robot.arm_left.move_to(positions["home"])

    pass


def job_grab_and_place_metal(robot, speech, visual):
    # - Yumi bewegt Arm-1 und greift das Metallteil
    # - Yumi bewegt Arm-1 und legt das Metallteil in den Verpresser
    # - Yumi bewegt Arm-1 zurück in die Startposition

    speech.print("Ich greife jetzt das Metallteil")
    
    robot.arm_left.move_to(positions["box_metal"])

    position_metal = visual.get_rubber()
    robot.arm_left.grab(position_metal)

    robot.arm_left.move_to(positions["tool_metal"])
    robot.arm_left.drop()

    robot.arm_left.move_to(positions["home"])

    pass


def job_move_tool_lever(robot, speech, visual):
    # - Yumi bewegt Arm-2 und hebt den Hebel hoch
    # - [Optional] Yumi bewegt Arm-2 und legt den Hebel um
    # - Yumi bewegt Arm-2 zurück in die Startposition

    speech.print("Ich lege jetzt den Hebel um")

    robot.arm_right.move_to(positions["tool_lever"])

    robot.arm_right.move_to(positions["tool_lever_down"])
    robot.arm_right.move_to(positions["tool_lever_up"])
    robot.arm_right.move_to(positions["tool_lever_down"])

    robot.arm_right.move_to(positions["home"])

    pass


def job_grab_and_place_finished_product(robot, speech, visual):
    # - Yumi bewegt Arm-2 und legt das fertige Produkt in eine Box
    # - Yumi bewegt Arm-2 zurück in die Startposition

    speech.print("Ich greife jetzt das fertige Bauteil")
    robot.arm_right.move_to(positions["tool_metal"])
    robot.arm_right.grab(positions["tool_metal"])

    speech.print("Ich lege jetzt das fertige Bauteil in die Box")
    robot.arm_right.move_to(positions["box_finished"])
    robot.arm_right.drop()

    robot.arm_right.move_to(positions["home"])

    pass


def job(robot, speech, visual) -> int:
    print("Hello, World!")

    # Master, Tread Sprachsteuerung, Thread Bewegung
    # -> Master ist 3 Wörter Erkennung, kann Thread Bewegung stoppen/pausieren/weiterführen
    # -> Status Flags für Objekt-Im-Greifer, wichtig für reset

    thread = threading.Thread(target=speech.listen)
    thread.daemon = True
    thread.start()

    running = True

    while running:
        job_grab_and_place_rubber()
        job_grab_and_place_metal()
        job_move_tool_lever()
        job_grab_and_place_finished_product()


def main() -> int:
    global positions
    positions_file = "./positions.json"

    print("Hello, World!")

    positions = Positions.from_file(positions_file)
    positions["root"] = Position.from_worldpoint(0, 0, 0)
    positions.to_file(positions_file)

    robot = robot_web_services.Robot()
    speech = speech_recognition.Speech()
    visual = visual_detection.Dectector()

    return job(robot, speech, visual)


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
