import numpy as np
from keras.models import load_model
from facenet.models import FaceVector
from .point import Face


model = load_model('pretrained_facenet_model')


def get_face_vector(face):
    face_temp = np.around(np.array(face) / 255.0, decimals=12)
    samples = np.expand_dims(face_temp, axis=0)
    face_vector = model.predict(samples)
    return face_vector


def vector_distance(face_vector):
    db_vectors = FaceVector.objects.all()
    values = []
    for dbv in db_vectors:
        v1 = dbv.get_vector
        dis = np.linalg.norm(face_vector - v1)
        data = {
            "distance": dis,
            "name": dbv.name
        }
        values.append(data)
    return values


def process_faces(face: Face, distances):
    min_dis = min(distances, key=lambda x: x['distance'])
    if min_dis["distance"] < 10:
        face.name = min_dis["name"]
        return face.json()
    return False


def create_facevector_db(name, face_vector):
    FaceVector.objects.create(
        name=name,
        vector=','.join([str(num) for num in face_vector.reshape(-1)])
    )
