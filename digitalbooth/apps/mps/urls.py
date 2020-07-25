from django.urls import path, include
from rest_framework.routers import DefaultRouter

from digitalbooth.apps.mps.views import MpsViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'mps', MpsViewSet, basename='mps')

urlpatterns = (
    path('', include(router.urls)),
)
