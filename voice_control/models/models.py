import platform
from os import path

this_platform = platform.system()
directory = path.dirname(path.realpath(__file__))

HEY_YUMI = path.join(directory, f"{this_platform}/Hey-Yu-Mi_de_{this_platform.lower()}_v2_2_0.ppn")
YUMI_STOP = path.join(directory, f"{this_platform}/Yu-Mi-Stop_de_{this_platform.lower()}_v2_2_0.ppn")
YUMI_WEITER = path.join(directory, f"{this_platform}/Yu-Mi-Weiter_de_{this_platform.lower()}_v2_2_0.ppn")

KEY_WORDS = ["HEY_YUMI", "YUMI_STOP", "YUMI_WEITER"]
KEY_WORDS_PATH = [HEY_YUMI, YUMI_STOP, YUMI_WEITER]

MODEL_PATH = path.join(directory, "porcupine_params_de.pv")
