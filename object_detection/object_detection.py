import sys

from robot_web_services.positions import Position


class ObjectDetector():
    def __init__(self): pass

    def get_rubber(self) -> Position:
        return Position.from_worldpoint(x=0, y=0, z=0)


    def get_metal(self) -> Position:
        return Position.from_worldpoint(x=0, y=0, z=0)


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
