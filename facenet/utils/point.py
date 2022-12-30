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
        self._confidence = confidence
        self._point_1 = Point(x1, y1)
        self._point_2 = Point(x2, y2)
        self._left_eye = Eye(*keypoints.get("left_eye"))
        self._right_eye = Eye(*keypoints.get("right_eye"))

    def json(self):
        return {
            "name": self._name,
            "confidence": self._confidence,
            "box": {
                "start": self._point_1.json(),
                "end": self._point_2.json(),
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

    def __str__(self) -> str:
        return f"Face({self._point_1}, {self._point_2})"
