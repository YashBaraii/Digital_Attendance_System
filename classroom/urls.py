from django.urls import path
from .views import (
    ClassroomListCreateAPIView,
    ClassroomUpdateDeleteAPIView,
    EnrollInClassAPIView
)

urlpatterns = [
    path('', ClassroomListCreateAPIView.as_view(), name='classroom-list-create'),
    path('<int:pk>/', ClassroomUpdateDeleteAPIView.as_view(), name='classroom-update-delete'),
    path('<int:pk>/enroll/', EnrollInClassAPIView.as_view(), name='classroom-enroll'),
]
