import logging
import sys

from robot_web_services.positions import Position


class GrabTarget:
    def __init__(self, position: Position, rotation: float):
        self.position = position
        self.rotation = rotation

    def get_grab_position(self) -> Position:
        # TODO: Calulate robtarget from self.position
        return Position.from_worldpoint(0, 0, 0)


class ObjectDetector:
    def __init__(self):
        pass

    def get_position_and_rotation(self) -> dict:
        # Example values for location of object
        return {"x": 960, "y": 540, "rotation": 180.0}

    def get(self, target) -> Position:
        if target not in ["rubber", "metal"]:
            raise ValueError(f"Unkown target: <{target}>")

        position_and_rotation = self.get_position_and_rotation()

        position = Position.from_worldpoint(
            x=position_and_rotation["x"], y=position_and_rotation["y"], z=0
        )
        rotation = position_and_rotation["rotation"]

        grab_target = GrabTarget(position, rotation)
        logging.debug(f"Grab target for <{target}> is: <{grab_target}>")

        grab_position = grab_target.get_grab_position()
        logging.debug(f"Grab position for <{target}> is: <{grab_position}>")

        return grab_position


def main() -> int:
    print("Hello, World")
    object_detector = ObjectDetector()

    position_rubber = object_detector.get("rubber")
    print(f"Gummiteil ist an Position <{position_rubber}>")

    position_metal = object_detector.get("metal")
    print(f"Metallteil ist an Position <{position_metal}>")

    return 0


if __name__ == "__main__":
    sys.exit(main())
