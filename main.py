import argparse
import datetime
import logging
import os
import pathlib
import signal
import sys
import threading

from config import CONFIG
from object_detection.object_detection import ObjectDetector
from robot_web_services.positions import Position, Positions
from robot_web_services.robot_web_services import RobotArm, RobotWebServices
from text_to_speech.text_to_speech import TextToSpeech
from voice_control.voice_control import VoiceControl


def configure_logger(logging_file, verbose: bool):
    level = logging.INFO if verbose is False else logging.DEBUG

    # Create directory and logfile if missing
    os.makedirs(os.path.dirname(logging_file), exist_ok=True)
    open(logging_file, "w+", encoding="utf-8").close()

    logger_stream_handler = logging.StreamHandler(sys.stdout)
    logger_stream_handler.setLevel(level)

    logger_file_handler = logging.FileHandler(logging_file)
    logger_file_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        format="%(asctime)s | [%(levelname)s] %(message)s",
        level=logging.DEBUG,
        handlers=[logger_stream_handler, logger_file_handler],
    )

    # TODO: Fix error message instead of suppresing it
    logging.raiseExceptions = False


class System:
    def __init__(self):
        logging.debug(f'[{CONFIG["Names"]["System"]}] [System] Startvorgang ...')

        logging.debug("Loading positions from file")
        self.positions = Positions.from_file(CONFIG["Positions"]["file"])

        logging.debug("Creating instance of RobotWebServices")
        self.robot = RobotWebServices(
            hostname=CONFIG["Robot Web Services"]["hostname"],
            username=CONFIG["Robot Web Services"]["username"],
            password=CONFIG["Robot Web Services"]["password"],
            model=CONFIG["Robot Web Services"]["model"],
        )
        self.robot.ready_robot()

        logging.debug("Creating instace of Dectector")
        self.detector = ObjectDetector()

        logging.debug("Creating instace of TextToSpeech")
        self.text_to_speech = TextToSpeech(
            top_level_domain=CONFIG["TextToSpeech"]["top_level_domain"],
            language=CONFIG["TextToSpeech"]["language"],
        )

        logging.debug("Creating instace of VoiceControl")
        self.voice_control = VoiceControl(
            porcupine_api_key=CONFIG["PORCUPINE"]["API_KEY"],
            openai_api_key=CONFIG["OPENAI"]["API_KEY"],
        )

        logging.debug(
            f'[{CONFIG["Names"]["System"]}] [System] Startvorgang abgeschlossen'
        )
        logging.info(
            f'[{CONFIG["Names"]["System"]}] System ready'
        )
    def _calibrate_arm(self, arm: RobotArm, positions: list[str]):
        for position in positions:
            message = f"Please move arm <{arm.name}> to position <{position}> and press <ENTER> ..."
            input(message)

            robtarget = arm.robtarget

            logging.debug(f"Setting position <{position}> to robtarget <{robtarget}>")
            self.positions[position] = Position.from_robtarget_class(robtarget)

        self.positions.to_file(CONFIG["Positions"]["file"])

    def calibrate(self):
        # TODO: Make calibration interactive, let use choose arm (l/r) and position (1/2/3/...)

        self._calibrate_arm(
            self.robot.arm_right,
            [
                "arm_right_box_metal",
                "arm_right_box_rubber",
                "arm_right_tool_metal",
                "arm_right_tool_rubber",
            ],
        )

        self._calibrate_arm(
            self.robot.arm_left,
            [
                "arm_left_box_finished",
                "arm_left_tool_lever_down",
                "arm_left_tool_lever_rotation_1",
                "arm_left_tool_lever_rotation_2",
                "arm_left_tool_lever",
                "arm_left_tool_metal",
            ],
        )

    def job_grab_rubber(self):
        message = "Ich greife jetzt das Gummiteil"
        self.text_to_speech.say(message)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}')

        self.robot.arm_right.move_to_home()
        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to(self.positions["arm_right_box_rubber"])

        position_rubber = self.detector.get("rubber")
        self.robot.arm_left.grab(position_rubber)

        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to_home()

    def job_place_rubber(self):
        message = "Ich lege jetzt das Gummiteil ab"
        self.text_to_speech.say(message)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}')

        self.robot.arm_right.move_to_home()

        self.robot.arm_right.move_to(self.positions["arm_right_tool_rubber"])
        self.robot.arm_left.drop()

        self.robot.arm_right.move_to_home()

    def job_grab_metal(self):
        message = "Ich greife jetzt das Metallteil"
        self.text_to_speech.say(message)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}')

        self.robot.arm_right.move_to_home()
        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])

        self.robot.arm_right.move_to(self.positions["arm_right_box_metal"])
        position_metal = self.detector.get("metal")
        self.robot.arm_left.grab(position_metal)

        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to_home()

    def job_place_metal(self):
        message = "Ich lege jetzt das Metallteil ab"
        self.text_to_speech.say(message)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}')

        self.robot.arm_right.move_to_home()

        self.robot.arm_right.move_to(self.positions["arm_right_tool_metal"])
        self.robot.arm_left.drop()

        self.robot.arm_right.move_to_home()

    def job_move_tool_lever(self):
        message = "Ich lege jetzt den Hebel um"
        self.text_to_speech.say(message)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}')

        self.robot.arm_left.move_to_home()

        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever"])
        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever_down"])
        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever_rotation_2"])

        self.robot.arm_left.move_to_home()

    def job_grab_finished_product(self):
        message = "Ich greife jetzt das fertige Bauteil"
        self.text_to_speech.say(message)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}')

        self.robot.arm_left.move_to_home()

        # TODO: Remove line: $ self.robot.arm_left.move_to(...)
        self.robot.arm_left.move_to(self.positions["arm_left_tool_metal"])
        self.robot.arm_left.grab(self.positions["arm_left_tool_metal"])

        self.robot.arm_left.move_to_home()

    def job_place_finished_product(self):
        message = "Ich lege jetzt das fertige Bauteil in die Box"
        self.text_to_speech.say(message)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}')

        self.robot.arm_left.move_to_home()

        self.robot.arm_left.move_to(self.positions["arm_left_box_finished"])
        self.robot.arm_left.drop()

        self.robot.arm_left.move_to_home()

    def start_voice_control(self):
        self.voice_control.start()

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
        self.ready_robot()

        self.voice_control.start()

        while True:
            task = self.voice_control.wait_for_task()

            if task == "YUMI_STOP":
                message = "Alles klar, ich stoppe."
                self.text_to_speech.say(message)
                logging.info(
                    f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}'
                )

            if task == "YUMI_WEITER":
                message = "Alles klar, ich mache weiter."
                self.text_to_speech.say(message)
                logging.info(
                    f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {message}'
                )

            if task == "ROBOT TASK 1":
                self.job_grab_rubber()
                self.job_place_rubber()

            if task == "ROBOT TASK 2":
                self.job_grab_metal()
                self.job_place_metal()

            if task == "ROBOT TASK 3":
                self.job_move_tool_lever()

            if task == "ROBOT TASK 4":
                self.job_grab_finished_product()
                self.job_place_finished_product()


def main(arguments) -> int:
    # print(f'[{CONFIG["Names"]["System"]}] Hello, World!')

    timestamp_date = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp_time = datetime.datetime.now().strftime("%H-%M-%S")
    logging_file = pathlib.Path(f"./logs/{timestamp_date}/{timestamp_time}.txt")
    configure_logger(logging_file, arguments.verbose)

    afv = System()

    def signal_handler(sig, frame):
        logging.debug(f"Received signal <{sig}> and frame <{frame}>")
        logging.info(f'[{CONFIG["Names"]["System"]}] System wird heruntergefahren')

        afv.robot.rapid_stop()

        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    if arguments.subparsers is None:
        if arguments.reset:
            return 0
        return afv.run()

    if arguments.subparsers == "debug":
        if arguments.voice_control:
            return afv.start_voice_control()
        if arguments.movement:
            return afv.start_movement()
        return afv.run()

    if arguments.subparsers == "calibrate":
        return afv.calibrate()

    return 0


if __name__ == "__main__":
    # Change directory to script location
    os.chdir(pathlib.Path(__file__).parent)

    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true", help="")
    parser.add_argument("-r", "--reset", action="store_true", help="")

    subparsers = parser.add_subparsers(dest="subparsers")

    subparser_1 = subparsers.add_parser("debug", help="")
    subparser_1.add_argument("-v", "--voice-control", action="store_true", help="")
    subparser_1.add_argument("-m", "--movement", action="store_true", help="")

    subparser_2 = subparsers.add_parser("calibrate", help="")

    args = parser.parse_args()

    # Run main()
    sys.exit(main(args))
