import logging
import os
import json
import pathlib
import sys
import threading
import datetime

from object_detection.object_detection import ObjectDetector
from robot_web_services.positions import Position
from robot_web_services.positions import Positions
from robot_web_services.robot_web_services import RobotWebServices
from text_to_speech.text_to_speech import TextToSpeech
from voice_control.voice_control import VoiceControl


# region global variables
positions = None
detector = None
robot = None
text_to_speech = None
voice_control = None
# endregion global variables


# region helper functions
def configure_and_get_logger(logging_file) -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)

    # Create directory and logfile if missing
    os.makedirs(os.path.dirname(logging_file), exist_ok=True)
    open(logging_file, 'w+').close()

    logger_file_handler = logging.FileHandler(logging_file)
    logger_file_handler.setLevel(logging.DEBUG)
    logger.addHandler(logger_file_handler)

    return logger
# endregion helper functions


# region jobs
def job_grab_and_place_rubber():
    global positions, detector, robot, text_to_speech, voice_control

    # - Yumi bewegt Arm-1 und greift das Gummiteil
    # - Yumi bewegt Arm-1 und "pudert" das Gummiteil
    # - Yumi bewegt Arm-1 und legt das Gummiteil in den Verpresser
    # - Yumi bewegt Arm-1 zurück in die Startposition

    text_to_speech.say("Ich greife jetzt das Gummiteil")
    
    robot.arm_left.move_to(positions["box_rubber"])

    position_rubber = detector.get_rubber()
    robot.arm_left.grab(position_rubber)

    robot.arm_left.move_to(positions["tool_rubber"])
    robot.arm_left.drop()

    robot.arm_left.move_to(positions["home"])

    pass


def job_grab_and_place_metal():
    global positions, detector, robot, text_to_speech, voice_control

    # - Yumi bewegt Arm-1 und greift das Metallteil
    # - Yumi bewegt Arm-1 und legt das Metallteil in den Verpresser
    # - Yumi bewegt Arm-1 zurück in die Startposition

    text_to_speech.say("Ich greife jetzt das Metallteil")
    
    robot.arm_left.move_to(positions["box_metal"])

    position_metal = detector.get_metal()
    robot.arm_left.grab(position_metal)

    robot.arm_left.move_to(positions["tool_metal"])
    robot.arm_left.drop()

    robot.arm_left.move_to(positions["home"])

    pass


def job_move_tool_lever():
    global positions, detector, robot, text_to_speech, voice_control

    # - Yumi bewegt Arm-2 und hebt den Hebel hoch
    # - [Optional] Yumi bewegt Arm-2 und legt den Hebel um
    # - Yumi bewegt Arm-2 zurück in die Startposition

    text_to_speech.say("Ich lege jetzt den Hebel um")

    robot.arm_right.move_to(positions["tool_lever"])

    robot.arm_right.move_to(positions["tool_lever_down"])
    robot.arm_right.move_to(positions["tool_lever_up"])
    robot.arm_right.move_to(positions["tool_lever_down"])

    robot.arm_right.move_to(positions["home"])

    pass


def job_grab_and_place_finished_product():
    global positions, detector, robot, text_to_speech, voice_control

    # - Yumi bewegt Arm-2 und legt das fertige Produkt in eine Box
    # - Yumi bewegt Arm-2 zurück in die Startposition

    text_to_speech.say("Ich greife jetzt das fertige Bauteil")
    robot.arm_right.move_to(positions["tool_metal"])
    robot.arm_right.grab(positions["tool_metal"])

    text_to_speech.say("Ich lege jetzt das fertige Bauteil in die Box")
    robot.arm_right.move_to(positions["box_finished"])
    robot.arm_right.drop()

    robot.arm_right.move_to(positions["home"])

    pass
# endregion jobs


def start_thread_voice_control():
    global positions, detector, robot, text_to_speech, voice_control

    # thread = threading.Thread(target=voice_control.listen)
    # thread.daemon = True
    # thread.start()

    pass


def start_thread_task():
    global positions, detector, robot, text_to_speech, voice_control

    running = True

    while running:
        job_grab_and_place_rubber()
        job_grab_and_place_metal()
        job_move_tool_lever()
        job_grab_and_place_finished_product()


def execute():
    global positions, detector, robot, text_to_speech, voice_control

    # Master, Tread Sprachsteuerung, Thread Bewegung
    # -> Master ist 3 Wörter Erkennung, kann Thread Bewegung stoppen/pausieren/weiterführen
    # -> Status Flags für Objekt-Im-Greifer, wichtig für reset

    start_thread_voice_control()
    start_thread_task()


def testing():
    global positions, detector, robot, text_to_speech, voice_control

    arm_left_position_1 = Position.from_robtarget(
        [
            [50, 210.610123632, 180.627879465],
            [0.066010741, 0.842421005, -0.11121506, 0.523068488],
            [0, 0, 0, 4],
            [141.502558998, 9e09, 9e09, 9e09, 9e09, 9e09],
        ]
    )
    arm_left_position_2 = Position.from_robtarget(
        [
            [60, 210.610123632, 180.627879465],
            [0.066010741, 0.842421005, -0.11121506, 0.523068488],
            [0, 0, 0, 4],
            [141.502558998, 9e09, 9e09, 9e09, 9e09, 9e09],
        ]
    )

    arm_right_position_1 = Position.from_robtarget(
        [
            [-9.578368507, -182.609892723, 198.627808149],
            [0.066010726, -0.842420918, -0.111214912, -0.523068661],
            [0, 0, 0, 4],
            [-135, 9e09, 9e09, 9e09, 9e09, 9e09],
        ]
    )
    arm_right_position_2 = Position.from_robtarget(
        [
            [-19.578368507, -182.609892723, 198.627808149],
            [0.066010726, -0.842420918, -0.111214912, -0.523068661],
            [0, 0, 0, 4],
            [-135, 9e09, 9e09, 9e09, 9e09, 9e09],
        ]
    )

    robot.arm_left.move_to(arm_left_position_1)
    robot.arm_left.move_to(arm_left_position_2)

    robot.arm_right.move_to(arm_right_position_1)
    robot.arm_right.move_to(arm_right_position_2)

    position = positions["home_arm_left"]
    robot.arm_right.move_to(position)


def main() -> int:
    print("Hello, World!")

    global positions, detector, robot, text_to_speech, voice_control

    config_file = pathlib.Path("./config.json")
    timestamp =  datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    logging_file = pathlib.Path(f"./logs/{timestamp}.txt")
    positions_file = pathlib.Path("./positions.json")

    logger = configure_and_get_logger(logging_file)

    if config_file.exists() == False:
        logger.critical("Config file is missing")
        raise Exception("Configuration file not found")

    with open(config_file, "r", encoding="utf-8") as config_file:
        logger.debug("Loading config from file")
        config = json.load(config_file)

    logger.debug("Loading positions from file")
    positions = Positions.from_file(positions_file)

    logger.debug("Creating instance of RobotWebServices")
    robot = RobotWebServices(
        hostname=config["Robot Web Services"]["hostname"],
        username=config["Robot Web Services"]["username"],
        password=config["Robot Web Services"]["password"],
        model=config["Robot Web Services"]["model"],
    )

    logger.debug("Creating instace of Dectector")
    detector = ObjectDetector()

    logger.debug("Creating instace of TextToSpeech")
    text_to_speech = TextToSpeech()

    logger.debug("Creating instace of VoiceControl")
    voice_control = VoiceControl()

    # TODO: Implement this
    # return execute()
    return testing()


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
