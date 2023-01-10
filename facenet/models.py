from django.db import models
import numpy as np


class FaceVector(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    vector = models.TextField()

    def __str__(self) -> str:
        return self.name

    @property
    def get_vector(self):
        vec = [float(v) for v in self.vector.split(",")]
        return np.asarray(vec, dtype=np.float32).reshape(1, -1)
