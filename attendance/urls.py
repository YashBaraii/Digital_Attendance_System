from django.urls import path
from .views import GenerateSessionQRView

urlpatterns = [
    path(
        "classrooms/<int:pk>/generate-session/",
        GenerateSessionQRView.as_view(),
        name="generate-session",
    ),
]
