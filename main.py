import argparse
import datetime
import logging
import os
import pathlib
import signal
import sys
import time

import system
from config import CONFIG


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


def main(arguments) -> int:
    # print(f'[{CONFIG["Names"]["System"]}] Hello, World!')

    timestamp_date = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp_time = datetime.datetime.now().strftime("%H-%M-%S")
    logging_file = pathlib.Path(f"./logs/{timestamp_date}/{timestamp_time}.txt")
    configure_logger(logging_file, arguments.verbose)

    system.initialize()

    def signal_handler(sig, frame):
        logging.debug(f"Received signal <{sig}> and frame <{frame}>")
        logging.info(f'[{CONFIG["Names"]["System"]}] System wird heruntergefahren')

        system.SYSTEM.robot.rapid_stop()

        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    if arguments.subparsers is None:
        if arguments.reset:
            system.SYSTEM.ready_robot()
            return 0

        system.SYSTEM.run()
        return 0

    if arguments.subparsers == "debug":
        CONFIG["DEBUG"] = True
        if arguments.voice_control:
            system.SYSTEM.debug_voice_control()
            return 0

        if arguments.movement:
            system.SYSTEM.debug_movement()
            return 0

        logging.warning("No debug routine selected")
        return 1

    if arguments.subparsers == "calibrate":
        system.SYSTEM.calibrate()
        return 0

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
