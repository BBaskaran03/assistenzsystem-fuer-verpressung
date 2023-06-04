import random
import threading
import time

import RWS

# Initialize communication with Norbert, start motors, and execute RAPID program
spongebob = RWS.RWS(base_url='http://localhost:80', username="Default User", password="robotics")

spongebob.request_mastership()
spongebob.motors_on()

def move_to_robtarget_left(robtarget: list[list[int]]):
    spongebob.start_RAPID()

    spongebob.set_rapid_variable_L("target", str(robtarget))
    print(f"Ready to move to {robtarget}")
    time.sleep(1)

    spongebob.set_rapid_variable_L("ready", "TRUE")
    print(f"Moving to {robtarget}")
    time.sleep(5)

    spongebob.stop_RAPID()

def move_to_robtarget_right(robtarget: list[list[int]]):
    spongebob.start_RAPID()

    spongebob.set_rapid_variable_R("target", str(robtarget))
    print(f"Ready to move to {robtarget}")
    time.sleep(1)

    spongebob.set_rapid_variable_R("ready", "TRUE")
    print(f"Moving to {robtarget}")
    time.sleep(5)

    spongebob.stop_RAPID()

move_to_robtarget_left([[50,210.610123632,180.627879465],[0.066010741,0.842421005,-0.11121506,0.523068488],[0,0,0,4],[141.502558998,9E+09,9E+09,9E+09,9E+09,9E+09]])
move_to_robtarget_left([[60,210.610123632,180.627879465],[0.066010741,0.842421005,-0.11121506,0.523068488],[0,0,0,4],[141.502558998,9E+09,9E+09,9E+09,9E+09,9E+09]])

move_to_robtarget_right([[-9.578368507,-182.609892723,198.627808149],[0.066010726,-0.842420918,-0.111214912,-0.523068661],[0,0,0,4],[-135,9E+09,9E+09,9E+09,9E+09,9E+09]])
move_to_robtarget_right([[-19.578368507,-182.609892723,198.627808149],[0.066010726,-0.842420918,-0.111214912,-0.523068661],[0,0,0,4],[-135,9E+09,9E+09,9E+09,9E+09,9E+09]])
