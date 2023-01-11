import numpy as np


class Point:
    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y
        self._point = np.array((x, y))

    def __sub__(self, other):
        return np.linalg.norm(self._point - other._point)

    def __str__(self) -> str:
        return f"Point({self._x},{self._y})"

    def json(self):
        return {
            "x": self._x,
            "y": self._y,
        }

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def point(self):
        return self._point


class Eye(Point):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)


class Face:
    def __init__(self, img, confidence, x1, y1, x2, y2, keypoints) -> None:
        self._img = img
        self._name = None
        self._distance = None
        self._confidence = confidence
        self._box_start = Point(x1, y1)
        self._box_end = Point(x2, y2)
        self._left_eye = Eye(*keypoints.get("left_eye"))
        self._right_eye = Eye(*keypoints.get("right_eye"))

    def json(self):
        return {
            "name": self._name,
            "confidence": self._confidence,
            "distance": self._distance,
            "box": {
                "start": self._box_start.json(),
                "end": self._box_end.json(),
            },
            "keypoints": {
                "left_eye": self._left_eye.json(),
                "right_eye": self._right_eye.json(),
            }
        }

    @property
    def left_eye(self):
        return self._left_eye

    @property
    def right_eye(self):
        return self._right_eye

    @property
    def box_start(self):
        return self._box_start

    @property
    def box_end(self):
        return self._box_end

    @property
    def box_center(self):
        _x = round((self._box_start.x + self._box_end.x)/2)
        _y = round((self._box_start.y + self._box_end.y)/2)
        return Point(_x, _y)

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, new_face_img):
        self._img = new_face_img

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, new_distance):
        self._distance = new_distance

    def __str__(self) -> str:
        return f"Face({self._box_start}, {self._box_end})"
