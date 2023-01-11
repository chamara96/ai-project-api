import mtcnn
from PIL import Image
import numpy as np
import math
from .point import Face, Point

ROTATE_CLOCKWISE = -1
ROTATE_COUNTER_CLOCKWISE = 1
NO_ROTATION = 0

detector = mtcnn.MTCNN()


def face_alignment(face: Face, original_img):
    if face.left_eye.y == face.right_eye.y:
        rotation_direction = NO_ROTATION
    elif face.left_eye.y > face.right_eye.y:
        point_c = Point(face.right_eye.x, face.left_eye.y)
        rotation_direction = ROTATE_CLOCKWISE
    else:
        point_c = Point(face.left_eye.x, face.right_eye.y)
        rotation_direction = ROTATE_COUNTER_CLOCKWISE

    face_img = face.img

    if rotation_direction != NO_ROTATION:
        edge_a = face.left_eye - point_c
        edge_b = face.right_eye - point_c
        edge_c = face.left_eye - face.right_eye

        if edge_b and edge_c:
            cos_a = (edge_b*edge_b + edge_c*edge_c - edge_a*edge_a)/(2*edge_b*edge_c)
            angle = np.arccos(cos_a)  # angle in radian
            angle = (angle * 180) / math.pi  # radian to degree

            if rotation_direction == ROTATE_CLOCKWISE:
                angle = 90 - angle

            face_center = face.box_center
            whole_img = Image.fromarray(original_img)
            rotated_img = np.array(
                whole_img.rotate(
                    angle=rotation_direction * angle,
                    center=(face_center.x, face_center.y)
                )
            )
            x1 = face.box_start.x
            y1 = face.box_start.y
            x2 = face.box_end.x
            y2 = face.box_end.y
            face_img = rotated_img[y1:y2, x1:x2]

    image = Image.fromarray(face_img)
    required_size = (160, 160)
    image = image.resize(required_size)
    face_array = np.asarray(image)
    face.img = face_array


def face_detector(image_mem_obj):
    with Image.open(image_mem_obj) as image:
        image = image.convert('RGB')
        img_array = np.asarray(image)

    faces = detector.detect_faces(img_array)
    faces_list = []
    for i, f in enumerate(faces):
        confidence = f["confidence"]
        if confidence > 0.95:
            x1, y1, width, height = faces[i]['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            keypoints = f["keypoints"]

            face_img = img_array[y1:y2, x1:x2]
            face = Face(face_img, confidence, x1, y1, x2, y2, keypoints)

            face_alignment(face, img_array)

            faces_list.append(face)

            # im = Image.fromarray(face.img)
            # im.save(f"face_{i}.jpeg")

    return faces_list
