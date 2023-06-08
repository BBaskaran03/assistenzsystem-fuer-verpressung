import collections
import json
import sys


class WorldPoint:
    def __init__(self, x, y, z):
        self.type = "relative"

        self.x = x
        self.y = y
        self.z = z

    @property
    def json(self):
        return self.__dict__

    def to_array(self):
        return [self.x, self.y, self.z]

    def __str__(self):
        return str(self.to_array())


class Rotation:
    def __init__(self, j1, j2, j3, j4, j5, j6):
        self.j1 = j1
        self.j2 = j2
        self.j3 = j3
        self.j4 = j4
        self.j5 = j5
        self.j6 = j6

    @property
    def json(self):
        return self.__dict__

    def to_array(self):
        return [self.j1, self.j2, self.j3, self.j4, self.j5, self.j6]

    def __str__(self):
        return str(self.to_array())


class ExternalAxesPosition:
    def __init__(self, a1, a2, a3, a4, a5, a6):
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a5 = a5
        self.a6 = a6

    @property
    def json(self):
        return self.__dict__

    def to_array(self):
        return [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]

    def __str__(self):
        return str(self.to_array())


class Orientation:
    def __init__(self, q1, q2, q3, q4):
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4

    @property
    def json(self):
        return self.__dict__

    def to_array(self):
        return [self.q1, self.q2, self.q3, self.q4]

    def __str__(self):
        return str(self.to_array())


class AxisConfiguration:
    def __init__(self, j1, j4, j6, jx):
        self.j1 = j1
        self.j4 = j4
        self.j6 = j6
        self.jx = jx

    @property
    def json(self):
        return self.__dict__

    def to_array(self):
        return [self.j1, self.j4, self.j6, self.jx]

    def __str__(self):
        return str(self.to_array())


class Jointtarget:
    def __init__(self, jointtarget: list[list[int]]):
        self.type = type
        self.rotation = Rotation(*jointtarget[0])
        self.external_axes_position = ExternalAxesPosition(*jointtarget[1])

    @property
    def json(self):
        json = {}

        try:
            json["rotation"] = self.rotation.json
        except AttributeError as e:
            pass

        try:
            json["external_axes_position"] = self.external_axes_position.json
        except AttributeError as e:
            pass

        return json

    def __str__(self) -> str:
        return str(self.json)


class Robtarget:
    def __init__(self, robtarget: list[list[int]]):
        self.worldpoint = WorldPoint(*robtarget[0])
        self.orientation = Orientation(*robtarget[1])
        self.axis_configuration = AxisConfiguration(*robtarget[2])
        self.external_axes_position = ExternalAxesPosition(*robtarget[3])

    @property
    def x(self):
        return self.worldpoint.x

    @property
    def y(self):
        return self.worldpoint.y

    @property
    def z(self):
        return self.worldpoint.z

    @property
    def json(self):
        json = {}

        try:
            json["worldpoint"] = self.worldpoint.json
        except AttributeError as e:
            pass

        try:
            json["orientation"] = self.orientation.json
        except AttributeError as e:
            pass

        try:
            json["axis_configuration"] = self.axis_configuration.json
        except AttributeError as e:
            pass

        try:
            json["external_axes_position"] = self.external_axes_position.json
        except AttributeError as e:
            pass

        return json

    def __str__(self) -> str:
        return str(self.json)


class PositionTarget:
    def __init__(self, robtarget: Robtarget):
        self._robtarget = robtarget

    def to_payload(self) -> str:
        txt = ""

        txt = f"{txt}pos-x={self._robtarget.worldpoint.x}&"
        txt = f"{txt}pos-y={self._robtarget.worldpoint.y}&"
        txt = f"{txt}pos-z={self._robtarget.worldpoint.z}&"

        txt = f"{txt}orient-q1={self._robtarget.orientation.q1}&"
        txt = f"{txt}orient-q2={self._robtarget.orientation.q2}&"
        txt = f"{txt}orient-q3={self._robtarget.orientation.q3}&"
        txt = f"{txt}orient-q4={self._robtarget.orientation.q4}&"

        txt = f"{txt}config-j1={self._robtarget.axis_configuration.j1}&"
        txt = f"{txt}config-j4={self._robtarget.axis_configuration.j4}&"
        txt = f"{txt}config-j6={self._robtarget.axis_configuration.j6}&"
        txt = f"{txt}config-jx={self._robtarget.axis_configuration.jx}&"

        txt = f"{txt}extjoint-1={self._robtarget.external_axes_position.a1}&"
        txt = f"{txt}extjoint-2={self._robtarget.external_axes_position.a2}&"
        txt = f"{txt}extjoint-3={self._robtarget.external_axes_position.a3}&"
        txt = f"{txt}extjoint-4={self._robtarget.external_axes_position.a4}&"
        txt = f"{txt}extjoint-5={self._robtarget.external_axes_position.a5}&"
        txt = f"{txt}extjoint-6={self._robtarget.external_axes_position.a6}&"

        return txt[:-1]


class Position(Jointtarget, Robtarget):
    def __init__(self):
        self.source = None

    # region classmethods
    @classmethod
    def from_worldpoint(cls, x, y, z):
        instance = Position()
        instance.source = "worldpoint"
        instance.worldpoint = WorldPoint(x, y, z)

        return instance

    @classmethod
    def from_rotation(cls, rotation):
        instance = Position()
        instance.source = "rotation"
        instance.rotation = Rotation(*rotation)

        return instance

    @classmethod
    def from_jointtarget(cls, jointtarget: list[list[int]]):
        instance = Jointtarget(jointtarget)
        instance.__class__ = Position
        instance.source = "jointtarget"
        instance.jointtarget = jointtarget

        return instance

    @classmethod
    def from_robtarget(cls, robtarget: list[list[int]]):
        instance = Robtarget(robtarget)
        instance.__class__ = Position
        instance.source = "robtarget"
        instance.robtarget = robtarget

        return instance

    @classmethod
    def from_robtarget_class(cls, robtarget: Robtarget):
        instance = robtarget
        instance.__class__ = Position
        instance.source = "robtarget"
        instance.robtarget = robtarget

        return instance

    # endregion classmethods

    @property
    def json(self):
        json = {"source": self.source}

        try:
            json["position"] = self.worldpoint.json
        except AttributeError as e:
            pass

        try:
            json["orientation"] = self.orientation.json
        except AttributeError as e:
            pass

        try:
            json["axis_configuration"] = self.axis_configuration.json
        except AttributeError as e:
            pass

        try:
            json["rotation"] = self.rotation.json
        except AttributeError as e:
            pass

        try:
            json["external_axes_position"] = self.external_axes_position.json
        except AttributeError as e:
            pass

        return json

    def to_array(self) -> list[list[int]]:
        array = [
            self.worldpoint.to_array(),
            self.orientation.to_array(),
            self.axis_configuration.to_array(),
            self.external_axes_position.to_array()
        ]

        return array

    def to_rapid_robtarget(self) -> str:
        robtarget = self.to_array()

        robtarget[3][1::] = ["9E+09", "9E+09", "9E+09", "9E+09", "9E+09"]
        robtarget = str(robtarget).replace(" ", "")
        robtarget = str(robtarget).replace("'", "")

        return robtarget

    def __str__(self):
        return str(self.json)


class Positions(collections.UserDict):
    @classmethod
    def from_file(cls, filename: str):
        with open(file=filename, mode="r", encoding="utf-8") as file:
            x = json.load(file)
            # y = {k: v for k, v in zip(x.keys(), x.keys())}
            y = Positions()

            for k, v in x.items():
                if "position" in v:
                    position = [
                        v["position"]["x"],
                        v["position"]["y"],
                        v["position"]["z"],
                    ]
                if "rotation" in v:
                    rotation = [
                        v["rotation"]["j1"],
                        v["rotation"]["j2"],
                        v["rotation"]["j3"],
                        v["rotation"]["j4"],
                        v["rotation"]["j5"],
                        v["rotation"]["j6"],
                    ]
                if "external_axes_position" in v:
                    external_axes_position = [
                        v["external_axes_position"]["a1"],
                        v["external_axes_position"]["a2"],
                        v["external_axes_position"]["a3"],
                        v["external_axes_position"]["a4"],
                        v["external_axes_position"]["a5"],
                        v["external_axes_position"]["a6"],
                    ]
                
                if "orientation" in v:
                    orientation = [
                        v["orientation"]["q1"],
                        v["orientation"]["q2"],
                        v["orientation"]["q3"],
                        v["orientation"]["q4"]
                    ]

                if "axis_configuration" in v:
                    axis_configuration = [
                        v["axis_configuration"]["j1"],
                        v["axis_configuration"]["j4"],
                        v["axis_configuration"]["j6"],
                        v["axis_configuration"]["jx"]
                    ]

                if v["source"] == "worldpoint":
                    y[k] = Position.from_worldpoint(*position)
                if v["source"] == "rotation":
                    y[k] = Position.from_rotation(rotation)
                if v["source"] == "jointtarget":
                    y[k] = Position.from_jointtarget([rotation, external_axes_position])
                if v["source"] == "robtarget":
                    y[k] = Position.from_robtarget([position, orientation, axis_configuration, external_axes_position])

            return y

    def to_file(self, filename: str):
        with open(file=filename, mode="w", encoding="utf-8") as file:
            json.dump(obj=self.json, fp=file, indent=4)

    @property
    def json(self):
        return {k: v.json for k, v in zip(self.keys(), self.values())}

    def __str__(self) -> str:
        return str(self.json)


def main() -> int:
    print("Hello, World")

    # region Unit-Tests Values
    worldpoint = [-8.578368507, -182.609892723, 198.627808149]
    rotation = [0, -130, 30, 0, 40, 0]
    orientation = [0.066010726, -0.842420918, -0.111214912, -0.523068661]
    axis_configuration = [0, 0, 0, 4]
    external_axes_position = [-135, 9e09, 9e09, 9e09, 9e09, 9e09]

    jointtarget = [[0, -130, 30, 0, 40, 0], [-135, 9e09, 9e09, 9e09, 9e09, 9e09]]
    robtarget = [
        [-8.578368507, -182.609892723, 198.627808149],
        [0.066010726, -0.842420918, -0.111214912, -0.523068661],
        [0, 0, 0, 4],
        [-135, 9e09, 9e09, 9e09, 9e09, 9e09],
    ]
    # endregion Unit-Tests Values

    # region Unit-Tests Helper
    worldpoint_class = WorldPoint(*worldpoint)
    rotation_class = Rotation(*rotation)
    orientation_class = Orientation(*orientation)
    axis_configuration_class = AxisConfiguration(*axis_configuration)
    external_axes_position_class = ExternalAxesPosition(*external_axes_position)
    jointtarget_class = Jointtarget([rotation, external_axes_position])
    robtarget_class = Robtarget(
        [worldpoint, orientation, axis_configuration, external_axes_position]
    )

    # print(worldpoint_class)
    # print(rotation_class)
    # print(orientation_class)
    # print(axis_configuration_class)
    # print(external_axes_position_class)
    # print(jointtarget_class)
    # print(robtarget_class)

    # endregion Unit-Tests Helper

    # region Unit-Tests class <Position>
    position_worldpoint = Position.from_worldpoint(*worldpoint)
    position_rotation = Position.from_rotation(rotation)
    position_jointtarget = Position.from_jointtarget(jointtarget)
    position_robtarget = Position.from_robtarget(robtarget)

    # print(position_worldpoint)
    # print(position_rotation)
    # print(position_jointtarget)
    # print(position_robtarget)
    # endregion Unit-Tests class <Position>

    # region Unit-Tests class <Positions>
    positions = Positions(
        {
            "position_worldpoint": position_worldpoint,
            "position_rotation": position_rotation,
            "position_jointtarget": position_jointtarget,
            "position_robtarget": position_robtarget,
        }
    )

    # print(positions)
    print(json.dumps(positions.json, indent=4))
    positions.to_file("./positions.json")

    del positions

    positions = Positions.from_file("./positions.json")
    print(json.dumps(positions.json, indent=4))

    # endregion Unit-Tests class <Positions>

    return 0


if __name__ == "__main__":
    sys.exit(main())
