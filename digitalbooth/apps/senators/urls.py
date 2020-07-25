from django.urls import path, include
from rest_framework.routers import DefaultRouter
from digitalbooth.apps.senators.views import SenatorsViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'senators', SenatorsViewSet, basename='senators')

urlpatterns = (
    path('', include(router.urls)),
)
