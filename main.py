import logging
import os
import json
import pathlib
import sys
import threading

from object_detection.object_detection import ObjectDetector
from robot_web_services.positions import Positions
from robot_web_services.robot_web_services import RobotWebServices
from text_to_speech.text_to_speech import TextToSpeech
from voice_control.voice_control import VoiceControl


# region helper functions
def configure_and_get_logger(logging_file) -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)

    # Create directory and logfile if missing
    os.makedirs(os.path.dirname(logging_file), exist_ok=True)
    open(logging_file, 'w+', encoding="utf-8").close()

    logger_file_handler = logging.FileHandler(logging_file)
    logger_file_handler.setLevel(logging.DEBUG)
    logger.addHandler(logger_file_handler)

    return logger
# endregion helper functions


class System():
    def __init__(self, config: dict, positions: Positions):
        self.logger = logging.getLogger(__name__)

        self.positions = positions

        self.logger.debug("Creating instance of RobotWebServices")
        self.robot = RobotWebServices(
            hostname=config["Robot Web Services"]["hostname"],
            username=config["Robot Web Services"]["username"],
            password=config["Robot Web Services"]["password"],
            model=config["Robot Web Services"]["model"],
        )
        self.robot.ready_robot()

        self.logger.debug("Creating instace of Dectector")
        self.detector = ObjectDetector()

        self.logger.debug("Creating instace of TextToSpeech")
        self.text_to_speech = TextToSpeech(
            top_level_domain=config["TextToSpeech"]["top_level_domain"],
            language=config["TextToSpeech"]["language"]
        )

        self.logger.debug("Creating instace of VoiceControl")
        self.voice_control = VoiceControl(
            porcupine_api_key=config["PORCUPINE"]["API_KEY"],
            openai_api_key=config["OPENAI"]["API_KEY"],
        )

    def job_grab_rubber(self):
        self.text_to_speech.say("Ich greife jetzt das Gummiteil")

        self.robot.arm_right.move_to_home()
        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to(self.positions["arm_right_rubber_box"])

        position_rubber = self.detector.get("rubber")
        self.robot.arm_left.grab(position_rubber)

        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to_home()

    def job_place_rubber(self):
        self.text_to_speech.say("Ich lege jetzt das Gummiteil ab")

        self.robot.arm_right.move_to_home()

        self.robot.arm_right.move_to(self.positions["arm_right_rubber_drop"])
        self.robot.arm_left.drop()

        self.robot.arm_right.move_to_home()

    def job_grab_metal(self):
        self.text_to_speech.say("Ich greife jetzt das Metallteil")

        self.robot.arm_right.move_to_home()
        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])

        self.robot.arm_right.move_to(self.positions["arm_right_metal_box"])
        position_metal = self.detector.get("metal")
        self.robot.arm_left.grab(position_metal)

        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to_home()

    def job_place_metal(self):
        self.text_to_speech.say("Ich lege jetzt das Metallteil ab")

        self.robot.arm_right.move_to_home()

        self.robot.arm_right.move_to(self.positions["arm_right_metal_drop"])
        self.robot.arm_left.drop()

        self.robot.arm_right.move_to_home()

    def job_move_tool_lever(self):
        self.text_to_speech.say("Ich lege jetzt den Hebel um")

        self.robot.arm_left.move_to_home()

        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever"])
        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever_down"])
        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever_up_2"])

        self.robot.arm_left.move_to_home()

    def job_grab_finished_product(self):
        self.text_to_speech.say("Ich greife jetzt das fertige Bauteil")

        self.robot.arm_left.move_to_home()

        # TODO: Remove line: $ self.robot.arm_left.move_to(...)
        self.robot.arm_left.move_to(self.positions["arm_left_tool_metal"])
        self.robot.arm_left.grab(self.positions["arm_left_tool_metal"])

        self.robot.arm_left.move_to_home()

    def job_place_finished_product(self):
        self.text_to_speech.say("Ich lege jetzt das fertige Bauteil in die Box")

        self.robot.arm_left.move_to_home()

        self.robot.arm_left.move_to(self.positions["arm_left_box_finished"])
        self.robot.arm_left.drop()

        self.robot.arm_left.move_to_home()

    def start_voice_control(self):
        self.voice_control.listen()

    def start_movement(self):
        running = True

        while running:
            self.job_grab_rubber()
            self.job_place_rubber()

            self.job_grab_metal()
            self.job_place_metal()

            self.job_move_tool_lever()

            self.job_grab_finished_product()
            self.job_place_finished_product()

            running = False

    def run(self):
        # TODO: Check for voice commands, if found, interact with robot
        voice_control = threading.Thread(target=self.start_voice_control)
        voice_control.start()

        movement = threading.Thread(target=self.start_movement)
        movement.start()


def main() -> int:
    print("Hello, World!")

    config_file = pathlib.Path("./config.json")
    timestamp =  datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    logging_file = pathlib.Path(f"./logs/{timestamp}.txt")
    positions_file = pathlib.Path("./positions.json")

    logger = configure_and_get_logger(logging_file)

    if not config_file.exists():
        logger.critical("Config file is missing")
        # pylint: disable-next=broad-exception-raised
        raise Exception("Configuration file not found")

    with open(config_file, "r", encoding="utf-8") as config_file:
        logger.debug("Loading config from file")
        config = json.load(config_file)

    logger.debug("Loading positions from file")
    positions = Positions.from_file(positions_file)

    return System(config, positions).run()


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Run main()
    sys.exit(main())
