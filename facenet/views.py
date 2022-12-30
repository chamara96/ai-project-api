from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser
from .serializers import ProcessImageSerializer, TrainFaceSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import face_detector, get_face_vector, vector_distance, process_faces, create_facevector_db
from rest_framework.decorators import api_view, action
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework import generics
from rest_framework import status



class FacenetView(GenericViewSet):
    """
    Facenet Process
    """
    parser_classes = [MultiPartParser]

    @action(detail=False, methods=['post'], serializer_class=ProcessImageSerializer)
    def process_image(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            image_mem_obj = serializer.validated_data["image"]
            faces = face_detector(image_mem_obj)
            identified_faces = []
            for f in faces:
                f_vec = get_face_vector(f.img)
                dis = vector_distance(f_vec)
                _face = process_faces(f, dis)
                if _face:
                    identified_faces.append(_face)
            data = {
                "faces": identified_faces,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=TrainFaceSerializer)
    def train_face(self, request):
        """
        Add new face into Database
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            image_mem_obj = serializer.validated_data["image"]
            face_name = serializer.validated_data["name"]
            face = face_detector(image_mem_obj)
            if len(face) == 0:
                data = {
                    "image": ["No face detected"]
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif len(face) == 1:
                train_face = face[0]
                train_face.name = face_name
                f_vec = get_face_vector(train_face.img)
                create_facevector_db(face_name, f_vec)
                data = {
                    "trained_face": train_face.json(),
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data = {
                    "image": ["Multiple faces detected"]
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
