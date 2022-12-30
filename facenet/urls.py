from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("v1", views.FacenetView, basename="v1")

urlpatterns = [
]

urlpatterns += router.urls
