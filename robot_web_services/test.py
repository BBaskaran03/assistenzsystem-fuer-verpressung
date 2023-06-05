import RWS
import random
import threading
from time import sleep
# Initialize communication with Norbert, start motors, and execute RAPID program
spongebob = RWS.RWS(base_url='http://localhost:80', username="Default User", password="robotics")  #Roboteranmeldung
spongebob.request_mastership()
spongebob.motors_on()
spongebob.start_RAPID()  # NB! Starts RAPID execution from main

# spongebob.get_rapid_variable_L("move")
# robtarget_pucks = spongebob.get_rapid_variable_L("puck_target")

# spongebob.set_rapid_variable_L("active", "TRUE")
spongebob.set_rapid_variable_L("target", "[[58.36296954,68.21461765,164.222908853],[0.338434022,0.713406389,-0.10353916,0.604808548],[0,0,0,4],[135,9E+09,9E+09,9E+09,9E+09,9E+09]]")

# x = input("x: ")
# y = input("y: ")
# z = input("z: ")
#sleep(5)
#spongebob.set_rapid_variable_L("puck_target", "[["+str(x)+","+str(y)+","+str(z)+"],[0.066010741,0.842421005,-0.11121506,0.523068488],[0,0,0,4],[141.502558998,9E+09,9E+09,9E+09,9E+09,9E+09]]")
#print(spongebob.set_rapid_variable_L("puck_target", "[[50,210.610123632,180.627879465],[0.066010741,0.842421005,-0.11121506,0.523068488],[0,0,0,4],[141.502558998,9E+09,9E+09,9E+09,9E+09,9E+09]]"))
#sleep(2)

#spongebob.set_rapid_variable_L("move", "FALSE")
# print(spongebob.get_rapid_variable_L("puck_target"))
# print(spongebob.get_gripper_position())

sleep(10)
spongebob.stop_RAPID()
