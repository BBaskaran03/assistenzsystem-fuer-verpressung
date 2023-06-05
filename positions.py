import os
import pathlib

from robot_web_services.positions import Position
from robot_web_services.positions import Positions

# Change directory to script location
os.chdir(pathlib.Path(__file__).parent)
positions_file = pathlib.Path("./positions.json")
positions = Positions.from_file(positions_file)

def add(name: str, robtarget: list[list[int]]):
    positions[name] = Position.from_robtarget(robtarget)

add("arm_right_home", [[-9.578368507,-182.609892723,198.627808149],[0.066010726,-0.842420918,-0.111214912,-0.523068661],[0,0,0,4],[-135,9E+09,9E+09,9E+09,9E+09,9E+09]])
add("arm_left_home", [[-9.578368507,182.609892723,198.627808149],[0.066010726,0.842420918,-0.111214912,0.523068661],[0,0,0,4],[135,9E+09,9E+09,9E+09,9E+09,9E+09]])

# del positions["somewhere"]

# for key, value in positions.items():
#     if value.json["source"] == "robtarget":
#         print(f'{key} => {value.to_rapid_robtarget()}')

print([position for position in positions])
positions.to_file(positions_file)
