from rest_framework import serializers
from .models import FaceVector


class ProcessImageSerializer(serializers.Serializer):
    image = serializers.ImageField(allow_empty_file=False)


class TrainFaceSerializer(ProcessImageSerializer):
    name = serializers.CharField(max_length=100, min_length=3, required=True)

    def validate(self, attrs):
        face_name = attrs.get("name")
        is_exists = FaceVector.objects.filter(name__iexact=face_name).exists()
        if is_exists:
            raise serializers.ValidationError(
                {
                    "name": "This name already exists in the database"
                }
            )
        return super().validate(attrs)
