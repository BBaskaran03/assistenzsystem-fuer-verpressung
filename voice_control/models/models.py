from os import path

__file_path = path.realpath(__file__)
__dir_path = path.dirname(__file_path)


__YUMI_STOP = path.join(__dir_path, "Yu-Mi-Stop_de_linux_v2_2_0.ppn")
__YUMI_WEITER = path.join(__dir_path, "Yu-Mi-Weiter_de_linux_v2_2_0.ppn")
__HEY_YUMI = path.join(__dir_path, "Hey-Yu-Mi_de_linux_v2_2_0.ppn")

MODEL_PATH = path.join(__dir_path, "porcupine_params_de.pv")

KEY_WORDS_PATH = [__YUMI_STOP, __YUMI_WEITER, __HEY_YUMI]
KEY_WORDS = [
    "YUMI_STOP",
    "YUMI_WEITER",
    "HEY_YUMI"
]
