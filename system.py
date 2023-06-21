import logging
import time

from config import CONFIG
from object_detection.object_detection import ObjectDetector
from robot_web_services.positions import Position, Positions
from robot_web_services.robot_web_services import RobotArm, RobotWebServices
from text_to_speech.text_to_speech import TextToSpeech
from voice_control.voice_control import VoiceControl


class System:
    def __init__(self):
        self.positions = None
        self.robot = None
        self.detector = None
        self.text_to_speech = None
        self.voice_control = None

    def log_debug(self, source: str, message: str):
        # logging.debug(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"][source]}> {message}')
        logging.debug(f'<{CONFIG["Names"][source]}> {message}')

    def log_info(self, source: str, message: str):
        # logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"][source]}> {message}')
        logging.info(f'<{CONFIG["Names"][source]}> {message}')

    def inform_user(self, source: str, message: str):
        self.log_info(source, message)
        self.text_to_speech.say(message)

    def inform_user_only_text(self, source: str, message: str):
        self.log_info(source, message)

    def ready_positions(self):
        logging.debug("Loading positions from file")
        self.positions = Positions.from_file(CONFIG["Positions"]["file"])

    def ready_robot(self):
        logging.debug("Creating instance of RobotWebServices")
        self.robot = RobotWebServices(
            hostname=CONFIG["Robot Web Services"]["hostname"],
            username=CONFIG["Robot Web Services"]["username"],
            password=CONFIG["Robot Web Services"]["password"],
            model=CONFIG["Robot Web Services"]["model"],
        )

        logging.debug("Running robot.ready_robot()")
        self.robot.ready_robot()
        logging.debug("Robot is ready")

    def ready_detector(self):
        logging.debug("Creating instace of Dectector")
        self.detector = ObjectDetector()

    def ready_text_to_speech(self):
        logging.debug("Creating instace of TextToSpeech")
        self.text_to_speech = TextToSpeech(
            top_level_domain=CONFIG["TextToSpeech"]["top_level_domain"],
            language=CONFIG["TextToSpeech"]["language"],
        )

    def ready_voice_control(self):
        logging.debug("Creating instace of VoiceControl")
        self.voice_control = VoiceControl(
            porcupine_api_key=CONFIG["PORCUPINE"]["API_KEY"],
            openai_api_key=CONFIG["OPENAI"]["API_KEY"],
        )

    def ready_system(self):
        self.log_info("System", "System wird gestartet ...")

        self.ready_positions()

        self.ready_robot()
        self.ready_detector()
        self.ready_text_to_speech()
        self.ready_voice_control()

        self.log_info("System", "System ist einsatzbereit")

    def shutdown(self):
        if CONFIG["DEBUG"]:
            self.inform_user_only_text("System", "System wird heruntergefahren")
        else:
            self.inform_user("System", "System wird heruntergefahren")

        if self.robot:
            self.robot.rapid_stop()

    def _calibrate_arm(self, arm: RobotArm, positions: list[str]):
        for position in positions:
            message = f"Please move arm <{arm.name}> to position <{position}> and press <ENTER> ..."
            input(message)

            robtarget = arm.robtarget

            logging.debug(f"Setting position <{position}> to robtarget <{robtarget}>")
            self.positions[position] = Position.from_robtarget_class(robtarget)

        self.positions.to_file(CONFIG["Positions"]["file"])

    def calibrate(self):
        self.ready_positions()
        self.ready_text_to_speech()
        self.ready_robot()

        # TODO: Make calibration interactive, let use choose arm (l/r) and position (1/2/3/...)

        self._calibrate_arm(
            self.robot.arm_right,
            [
                "arm_right_box_metal",
                "arm_right_box_rubber",
                "arm_right_checkpoint",
                "arm_right_tool_metal_above",
                "arm_right_tool_metal",
                "arm_right_tool_rubber_above",
                "arm_right_tool_rubber",
            ],
        )

        self._calibrate_arm(
            self.robot.arm_left,
            [
                "arm_left_box_finished",
                "arm_left_checkpoint",
                "arm_left_tool_lever_down",
                "arm_left_tool_lever_rotation_1",
                "arm_left_tool_lever_rotation_2",
                "arm_left_tool_lever",
                "arm_left_tool_metal",
            ],
        )

    def job_grab_rubber(self):
        message = "Ich greife jetzt das Gummiteil"
        self.inform_user("Robot", message)

        self.robot.arm_right.move_to_home()
        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to(self.positions["arm_right_box_rubber"])

        self.robot.arm_right.gripper_open()

        try:
            # pylint: disable-next=unused-variable
            position_rubber = self.detector.get("rubber")
            # self.robot.arm_right.grab(position_rubber)
            time.sleep(2)

        # pylint: disable-next=broad-exception-caught,unused-variable
        except Exception as exception:
            logging.critical('self.detector.get("rubber")')
            # logging.debug(exception)

        self.robot.arm_right.gripper_close()

        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to_home()

    def job_place_rubber(self):
        message = "Ich lege jetzt das Gummiteil ab"
        self.inform_user("Robot", message)

        self.robot.arm_right.move_to_home()

        self.robot.arm_right.move_to(self.positions["arm_right_tool_rubber_above"])
        self.robot.arm_right.move_to(self.positions["arm_right_tool_rubber"])
        self.robot.arm_right.gripper_open()

        self.robot.arm_right.move_to_home()

    def job_grab_metal(self):
        message = "Ich greife jetzt das Metallteil"
        self.inform_user("Robot", message)

        self.robot.arm_right.move_to_home()
        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])

        self.robot.arm_right.move_to(self.positions["arm_right_box_metal"])

        self.robot.arm_right.gripper_open()

        try:
            # pylint: disable-next=unused-variable
            position_metal = self.detector.get("metal")
            # self.robot.arm_right.grab(position_metal)
            time.sleep(2)

        # pylint: disable-next=broad-exception-caught,unused-variable
        except Exception as exception:
            logging.critical('self.detector.get("metal")')
            # logging.debug(exception)

        self.robot.arm_right.gripper_close()

        self.robot.arm_right.move_to(self.positions["arm_right_checkpoint"])
        self.robot.arm_right.move_to_home()

    def job_place_metal(self):
        message = "Ich lege jetzt das Metallteil ab"
        self.inform_user("Robot", message)

        self.robot.arm_right.move_to_home()

        self.robot.arm_right.move_to(self.positions["arm_right_tool_metal_above"])
        self.robot.arm_right.move_to(self.positions["arm_right_tool_metal"])
        self.robot.arm_right.gripper_open()

        self.robot.arm_right.move_to_home()

    def job_move_tool_lever(self):
        message = "Ich lege jetzt den Hebel um"
        self.inform_user("Robot", message)

        self.robot.arm_left.move_to_home()

        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever"])
        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever_down"])
        self.robot.arm_left.move_to(self.positions["arm_left_tool_lever_rotation_2"])

        self.robot.arm_left.move_to_home()

    def job_grab_finished_product(self):
        message = "Ich greife jetzt das fertige Bauteil"
        self.inform_user("Robot", message)

        self.robot.arm_left.move_to_home()

        # TODO: Remove line: $ self.robot.arm_left.move_to(...)
        self.robot.arm_left.move_to(self.positions["arm_left_tool_metal"])

        self.robot.arm_left.gripper_open()

        # self.robot.arm_left.grab(self.positions["arm_left_tool_metal"])
        time.sleep(2)

        self.robot.arm_left.gripper_close()

        self.robot.arm_left.move_to_home()

    def job_place_finished_product(self):
        message = "Ich lege jetzt das fertige Bauteil in die Box"
        self.inform_user("Robot", message)

        self.robot.arm_left.move_to_home()

        self.robot.arm_left.move_to(self.positions["arm_left_box_finished"])
        self.robot.arm_left.gripper_open()

        self.robot.arm_left.move_to_home()

    def debug_movement(self):
        self.ready_positions()

        self.ready_robot()
        self.ready_detector()
        self.ready_text_to_speech()

        self.job_grab_rubber()
        self.job_place_rubber()

        self.job_grab_metal()
        self.job_place_metal()

        self.job_move_tool_lever()

        self.job_grab_finished_product()
        self.job_place_finished_product()

    def debug_voice_control(self):
        self.ready_text_to_speech()
        self.ready_voice_control()

        if not CONFIG["DEBUG"]:
            self.voice_control.start()

        while True:
            task = self.voice_control.wait_for_task()
            logging.info(f"Reacting to <{task}>")

    def run(self):
        self.ready_system()

        self.voice_control.start()

        while True:
            task = self.voice_control.wait_for_task()

            if task == "YUMI_STOP":
                message = "Alles klar, ich stoppe."
                self.inform_user("Robot", message)

            if task == "YUMI_WEITER":
                message = "Alles klar, ich mache weiter."
                self.inform_user("Robot", message)

            # TODO: Fix ChatGPT not responding with <ROBOT TASK X> only

            if task.startswith("ROBOT TASK 1"):
                self.job_grab_rubber()
                self.job_place_rubber()

            if task.startswith("ROBOT TASK 2"):
                self.job_grab_metal()
                self.job_place_metal()

            if task.startswith("ROBOT TASK 3"):
                self.job_move_tool_lever()

            if task.startswith("ROBOT TASK 4"):
                self.job_grab_finished_product()
                self.job_place_finished_product()


SYSTEM = None


def initialize():
    # pylint: disable-next=global-statement
    global SYSTEM

    SYSTEM = System()
