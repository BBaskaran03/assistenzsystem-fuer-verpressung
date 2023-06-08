import sys

from robot_web_services.positions import Position, Robtarget


class GrabTarget:
    def __init__(self, position: Position, rotation: float):
        self.position = position
        self.rotation = rotation

    def get_grab_position() -> Position:
        # TODO: Calulate robtarget from self.position
        return Position.from_robtarget(None)


class ObjectDetector:
    def __init__(self):
        pass

    def get_rubber(self) -> Position:
        # Example values for location of object
        position_pixel = {"x": 960, "y": 540}
        rotation = 180.0

        position = Position.from_worldpoint(
            x=position_pixel["x"], y=position_pixel["y"], z=0
        )

        grab_target = GrabTarget(position, rotation)
        return grab_target.get_grab_position()

    def get_metal(self) -> Position:
        # Example values for location of object
        position_pixel = {"x": 960, "y": 540}
        rotation = 180.0

        position = Position.from_worldpoint(
            x=position_pixel["x"], y=position_pixel["y"], z=0
        )

        grab_target = GrabTarget(position, rotation)
        return grab_target.get_grab_position()


def main() -> int:
    print("Hello, World")
    object_detector = ObjectDetector()

    position_rubber = object_detector.get_rubber()
    print(f"Gummiteil ist an Position <{position_rubber}>")

    position_metal = object_detector.get_metal()
    print(f"Metallteil ist an Position <{position_metal}>")

    return 0


if __name__ == "__main__":
    sys.exit(main())
